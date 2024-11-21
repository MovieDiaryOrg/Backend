from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieJournalSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MovieJournal, MovieEvaluation, Recommended
from movies.models import Movie, Genre, MovieGenre
from django.conf import settings
from openai import OpenAI
import json


"""
ModelViewSet은 기본적인 CRUD 작업을 제공하며, 
커스텀 동작이 필요하다면 ViewSet의 메서드를 오버라이드하거나 @action 데코레이터를 사용해야 함.
"""

class MovieJournalViewSet(ModelViewSet):
    queryset = MovieJournal.objects.all()
    serializer_class = MovieJournalSerializer
    permission_classes = [IsAuthenticated]          # 인증된 사용자만 접근 가능함
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dalle_prompt = ''  # 인스턴스 속성으로 dalle_prompt 선언
        self.movie_journal = None
        self.OPENAI_API_KEY = settings.OPENAI_API_KEY

    # ModelViewSet 클래스가 상속받는 mixins.CreateModelMixin 클래스의 create() 오버라이딩
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.movie_journal = self.perform_create(serializer)             # MovieJournal 객체 생성 및 DB 저장

        # 예외 처리
        if not self.movie_journal:
            raise ValueError("MovieJournal 객체 생성에 실패했습니다.")

        # print(f'serializer.data = {serializer.data}')
        print(f'movie_journal = {self.movie_journal}')

        # OpenAI API를 이용해 감상문 분석    
        self.create_ai_analystic(serializer.data['content'])

        # OpenAI API를 이용해 그림 생성
        self.create_ai_img()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # mixin.CreateModelMixin 클래스 내부 메소드 오버라이딩
    def perform_create(self, serializer):
        journal = serializer.save()
        return journal
    

    def create_ai_analystic(self, content):
        """
        OpenAI API를 이용해 추천 영화 및 그림 생성 프롬프트 생성
        """
        client = OpenAI(api_key=self.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {
                    "role": "system",
                    "content": "아래 기준에 따라 영화 리뷰를 분석하여 리뷰어의 만족도를 분석하세요. 응답은 반드시 JSON 객체여야 하며, JSON 스키마는 response_format를 따릅니다. 그리고 이어서 볼 만한 실제 영화 세 편을 추천하고, 영화 개봉일과 추천 이유를 포함하여 작성하세요. 그리고 DALL.E에게 리뷰에 담긴 리뷰어의 감정이나 영화의 줄거리를 잘 설명하는 그림을 요청하기 위한 프롬프트를 작성합니다. 그림의 스타일은 색연필이나 크레용으로 그려진 그림입니다. 1. Positive words describe feelings: good, great, inspiring, funny, enjoyable, enjoyable, cool, impressive, impressive, great, lovely, fascinating. Evaluate a movie: perfect, artistic, engaging, entertaining, emotional, fresh, moving, intense, shocking, admire, impressive. Acting/Characters: Great acting, naturalistic, characters come alive, relatable, realistic, great characters, fits the part, well acted. Directing/Composition: Interesting, thrilling, well-structured, perfectly directed, engaging, rhythmic, stylishly directed, original, novel. 2. negative words express emotions: disappointing, not good, unfortunate, boring, unpleasant, childish, awkward, unnecessary, unreasonable. Evaluate the movie: unrealistic, flimsy, lacking, predictable, clichéd, distracting, disappointing, old, outdated. Acting/Characters: Unnatural, out of place, forced, exaggerated, unsympathetic, hard to understand, unlikable. Directing/Composition: Loose, predictable, convoluted, wordy, esoteric, uninvolving, sloppy, exhausting. 3. neutral words express anticipation: anticipated, unexpected, surprising, twist, mystery, meaningful, thought-provoking. Evaluate the movie: decent, unique, independent, emotional, lingering, noteworthy, noteworthy. Acting/Characters: Acting, Characterization, Acting, Symbolic. Directing/Composition: Epic, well organized, well directed, has style'"
                },
                {
                    "role": "user",
                    "content": "미뤄뒀던 감상 후기를 적어보려고 한다. 엄마가 토요일에 출국이시라 짐싸는 걸 돕기 위해 마산으로 내려왔다. 오는 길에 운전하면서 여러모로 스트레스가 굉장했어서 마음을 풀 만한 걸 찾고있었는데 문득 얼마 전에 '정리해둬야지~ 해둬야지~' 했던 <오펜하이머> 감상 후기가 생각나서 이참에 작성해볼까 한다. 오랜만에 츄와 창원에서 데이트를 하기로 했다. 뭘할까 고민했지만 더운 여름에 할 만한 건 역시나 영화 감상이었다. 선택지가 많진 않았지만 그 중에 우리가 꼭 보고싶었던 <오펜하이머>를 보러 가게 됐다. 츄가 이 영화에 대해 처음 설명을 해줬을 때 간단히 '핵폭탄을 처음 개발한 사람에 대한 영화'라고 말해줬었다. 그래서 역사적으로 중요한 인물이라는 생각에 교양 쌓기에도 좋겠다 싶었다. 영화를 보기로 한 날, 창원 롯데백화점 지하 크리스피크림 매장에서 우린 커피와 도넛을 먹으며 영화 감상을 위한 간단한 몸풀기(?)를 하고 있었다. 츄는 침착맨이 궤도라는 물리 박사님과 함께 '오펜하이머 감상 전에 보고 가면 좋은 영상'을 올렸다며 함께 보자고 했다. 그렇게 약 30분 가량을 무슨 말인지도 모르고 영상을 함께 시청했고, 영화 시간이 다되어 우리는 팝콘을 사들고 상영관으로 향했다. 영화는 3시간 분량으로 영화치고는 많이 긴 편에 속했는데, 모든 장면이 인상 깊어 조금도 지루하지 않았다. 정말 내 인생 통틀어 손꼽을 수 있는 웰메이드 영화라는 생각이 들었다. 한 영화를 여러 번 감상하는 걸 좋아하지 않는 내가 이 영화만큼은 다시 한번 꼭 보고싶다는 생각이 들 정도로. 츄가 보자고 했던 침착맨의 영상이 없었다면 이렇게 흥미진진하게 감상하지 못했을 수도 있지만..🙄ᄒ 인상 깊었던 장면을 몇 가지 꼽아보자면, 1. 보안 승인 심사 비공식 청문회에서 오펜하이머는 완전히 발가벗겨졌다. 나는 비공식 청문회에서 오펜하이머를 추궁하던 사법 기관 관계자들 모두 그 자리에서 민낯을 드러낸 것이라고 생각한다. 원자폭탄 실험이 성공하고, 미국은 그 위력을 세계에 보여주고자 타겟을 물색하고 있었다. 그와중에 미국의 눈에 띈 건 바로 일본. 전쟁이 끝나기 전 본인들의 역량을 알리고자 다급해진 미국은 일본의 히로시마와 나가사키에 지체없이 원자 폭탄을 투하한다. 성공적인 작전 이후 오펜하이머는 잠시나마 죄책감에 시달리지만, 모두가 본인을 전쟁 영웅으로 떠받드는 모습에 본인도 모르게 심취하게 된다. 하지만 그런 와중에서도 오펜하이머는 원자 폭탄의 위력이 세계 모두를 위험에 빠뜨릴 수 있음을 알고 향후 수소폭탄 개발에 대해 반대 입장을 취하게 된다. 이에 많은 동료 학자들이 등을 돌리기도 했다. 그리고 시간이 흘러 오펜하이머의 보안 심사 재승인을 위한 비공식 청문회가 열리게 되는데, 그곳에서 오펜하이머에 대한 질투로 그를 끝내 무너뜨리고자 했던 스트로스 제독(이자 AEC, 미국 원자력 의회 의장)의 의도대로 롭 검사는 오펜하이머의 사생활까지 들추며 그의 자질을 의심한다. 그리고 영화에서는 장면이 전환되며 오펜하이머가 청문회에서 벌거벗고 앉아있는 모습이 등장한다. 하지만 그 장면을 보고 나는 오히려 그 자리의 모두가 옷이 벗겨진 것이란 생각이 들었다. 그 자리에는 그 누구도 이성적으로 그 상황을 끌고가려는 자가 없었다. 롭 검사를 비롯해 스트로스 제독에 의해 청문회 위원으로 발탁된 사람들 모두 일방적인 마녀 사냥을 통해 스트로스 제독이 의도한 결말로 이끌어 가고자 혈안이 되어있었다. 치사하게도 오펜하이머의 변호인에게 자료조차 제공하지 않았고, 비꼬는 듯한 말로 오펜하이머를 끝까지 도발하고 자극했다. 그들 모두 개인적인 이익을 위해 진실을 보지 않기로 선택한 것이다. 어느 누구도 제대로된 인간으로서 도리를 지키고자 한 자가 없었다. 오펜하이머의 동료로 참석하게된 여러 학자들 역시 끝내 오펜하이머에게 보안 심사 승인은 해줄 수 없을 것 같다고 증언했다. 그들 역시 개인적인 감정이 있었거나 혹은 그 자리가 끝난 후 혹시나 오게 될 부정적 피드백이 두려워서 그랬을 것이다. 마지막으로 오펜하이머의 와이프 키티는 청문회가 시작되기 전까진 냉철한 모습을 지켰으나, 본인의 공산주의집단 활동 이력이 들통나자 순간적으로 감정을 조절하지 못하는 모습을 보였다. 하지만 끝까지 이성을 잃지 않은 사람은 그나마 키티였던 게 아닌가 싶다. 청문회를 통해 오펜하이머는 과학자로서 논리적이지 못한 본인의 감정적 내면을 드러내게됨과 동시에 사생활까지 들춰지게 됐지만, 반대로 청문회 위원들은 모두가 진실을 외면한 채 오로지 각자의 이익을 위해 내달리는 탐욕적인 본모습을 내비춘 자리였다고 생각이 들었다. 2. 아인슈타인은 오펜하이머에게 '언젠가 그들이 구운 연어와 감자 샐러드를 대접하며 목에 메달을 걸어줄 것입니다. 그리고 다가와 어깨를 두드릴 거예요. 하지만 잊지마세요. 그 자리의 주인공은 당신이 아니라 그들이라는 것을' 이라고 말한다. 정말 목에 메달을 걸어줄 만큼 그 사람을 인정해서가 아니라, 메달을 걸어주는 그들에게 단지 메달을 목에 거는 그 존재가 필요했을 뿐이라는 것. 그 상황의 의도를 파악하고 선을 넘지 않도록 주의해야 한다는 것. 나는 이것이 인간의 외로운 삶을 보여주는 말이라고 생각했다. 인간은 모두 서로를 이용하며 살아간다. 살아가다보면 상대가 나를 이용하고 있음을 알면서도 웃으면서 이용당해야하는 상황이 종종 연출된다. 반대로 내가 필요할 땐 언젠가 저 사람을 이용하겠다 생각하면서. 그로 인해 인간 모두는 내면에 깊은 외로움을 가지고 살아가는 것 같다. 나는 저 말이 그 외로움을 아주 잘 표현한 말이라고 생각했다. 그리고 인간은 그 외로움을 받아들여야 한다는 것을 알려주는 것만 같았다. 매일 공부만 하는 학자마저 인간관계의 그 깊은 이면을 꼬집을 수 있을 정도라니.. 어느 세계이건 사람 관계는 참 어려운가보다. 인간관계는 평생의 숙제라는 말이 있던데, 그 숙제를 모두 풀고 가는 사람이 있을까? 3. 오펜하이머의 부인 키티는 아주 이성적이고 지혜로운 여성이다. 캐서린 키티 오펜하이머는 오펜하이머의 외도 사실을 알고도 그에게 '정신차리라'고 말한다. 그의 어깨에 국가의 중대한 임무가 놓여있음을 알았기 때문인지, 오펜하이머가 지휘자로서 역할을 잘해낼 수 있게 끝까지 곁을 지키기까지 한다. 나는 그녀가 이 영화 속에서 가장 지혜로운 인물이었다고 생각한다. 그녀는 평소에는 한낱 감정적인 인간이었다가도 중요한 순간엔 항상 본질적으로 중요한 것이 무엇인지를 볼 줄 아는 눈이 있었다. 그녀는 남편인 오펜하이머의 청문회에 증언하고자 불려간 자리에서 본인의 과거는 물론 남편의 외도 사실이 온 나라에 까발려졌음에도 불구하고 그의 손을 잡고 남은 여생을 함께 보내는 모습을 보여준다. 오펜하이머가 그런 치욕스러운 시간을 견딜 수 있었던 건 모두 아내 덕이 아니었을까 생각이 들었다. 무슨 일이 생겨도 본인 곁을 지켜주는 한 사람이 있다는 건 삶에서 나를 버티게 하는 아주 큰 힘이 된다. 근데 오펜하이머에겐 그 사람이 바로 키티였던 것 같다. 오펜하이머를 버틸 수 있게 지켜준 그녀가 없었다면 영화 <오펜하이머>의 결말이 아주 달라지지 않았을까. 4. 오펜하이머를 시기한 루이스 스트로스 제독은 끝내 더러운 본심을 드러내게 된다. 루이스 스트로스 제독은 AEC(미국 원자력 의회) 의장으로, 오펜하이머의 오만한 농담으로 당하게된 망신과 오펜하이머와의 대화 이후 본인의 인사를 무시하는 아인슈타인을 보곤 오펜하이머를 증오하게 된다. 그 일을 마음 속에 담아두고 있던 스트로스 제독은 비밀리에 공권력을 동원하여 오펜하이머를 압박하고 망신주려 한다. 하지만 이를 들키게 되며 상무부 장관 인사청문회 결과 심사 탈락하게 된다. 나는 오펜하이머를 직접 만나서도 거짓 얼굴로 그를 위하는 척하던 스트로스 제독이 결국 더러운 본심을 내보이며 추락하는 모습을 보이는 이 장면이 정말 마음에 들었다. 권선징악 스토리여서 그런 걸까. 아무리 좋은 포장지로 감싸도 결국에 그 속에 있는 더러운 본심은 드러나기 마련이라는 메시지를 주는 것 같아 영화를 보며 정말 짜릿한 순간이었다. 5. 영화의 마지막 즈음에 오펜하이머의 동료가 '이 비공식 청문회는 이길 수 없는 마녀사냥이다.'라고 말할 때, 오펜하이머는 '그걸 알면서도 견디는 것은 이유가 있지 않겠나.' 하고 대답한다. 마녀사냥임을 알면서도 견디는 이유는 바로 본인의 죄책감 때문이 아니었을까. 전쟁이 끝나고 전쟁 영웅으로 칭송 받던 오펜하이머는 잠깐 그 영광에 취한 것은 맞지만 결코 그 죄책감을 잊은 적은 없었던 것 같다. 그리고 그 죗값을 이 청문회를 통해 치르는 것이라 생각했던 게 아닐까. 본인이 추락하게 될 것임을 알면서도 우직하게 그저 견디고만 있던 모습이 안쓰러울 정도로 담담해보였던 걸 보면. 오펜하이머는 비공식 청문회에서 숨기고 싶은 사생활이 까발려지면서도 수소 폭탄은 끝까지 반대했다. 그는 본인의 죄책감 때문인지 수소 폭탄만큼은 찬성할 수 없다는 입장을 고수했다. 그러나 수소 폭탄을 연구해보고 싶다는 동료 학자에게 그 어떤 비난도 어떤 강요도 하지 않았다. 오히려 그 의견을 존중했다. 그리고 그럼에도 불구하고 본인의 소신 또한 굽히지 않았고, 그 소신대로 행동하고자 끝까지 노력했다. 영화 초반에 보면 오펜하이머에 대해 학문적으로 일은 잘 하나, 인간 관계에선 약간 서툴다는 식의 대사가 몇 나온다. 그리고 흑백의 비공개 청문회 장면이 나올 때마다 오펜하이머는 '바보같다'는 생각이 들 정도로 가만히 당하고만 있는 모습이 나온다. 하지만 본인의 소신을 지키고 또 그것대로 행동하기 위해 마지막까지 노력하는 오펜하이머를 보면, 결코 단순히 순진함으로 인해 그 모든 상황을 견딘 것은 아님을 알 수 있다. 살아가면서 단순히 생각하는 것과 실제로 그 생각대로 행동하는 것은 완전히 다른 문제이기 때문이다. 오펜하이머는 이기적이고 사람 다룰 줄 모른다는 말을 들을 만큼 본인의 학문이 중요한 사람이었지만, 누구보다 솔직하고 당당했으며 본인의 순수한 고집을 지키고자 마지막까지 노력한, 바보같을 정도로 깨끗한 사람이었다고 생각이 든다. 전쟁 종료 이후 영광에 심취해 잠시나마 죄책감을 잊어버리는 모습도, 누구보다 이성적이고 논리적인 학문을 다루는 사람이 비논리적인 감정의 흐름을 아주 솔직하게 내비추는 그 장면도, 그리고 뒤늦게서 메달을 목에 걸어주며 등을 두드려주는 그 모두에게 웃어줄 줄 아는 그가 정말 누구보다 순수하고 겸손했던 사람이라는 것을 이 영화를 통해 알 수 있었던 것 같다. 3시간의 긴 러닝타임이었지만 단 한 장면도 놓치고 싶지 않을 정도로 깊이있는 영화였다. 두 눈 부릅뜨고 봤었지만 분명히 내가 놓친 의미들이 있을테니 꼭 한 번 더 봐야겠다 싶다. 오랜만에 정말 좋은 영화 감상이었다."
                }
            ],
            
            response_format = {
                "type": "json_schema",
                "json_schema" : {
                    "name": "diary_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "analysis": {
                                "type": "string",
                                "description": "A detailed analysis of the movie review."
                            },
                            "movie_recommendations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties":{
                                        "title": {
                                            "type": "string",
                                            "description": "The title of the recommended movie."
                                        },
                                        "release_date" :{
                                            "type": "string",
                                            "description": "The release date of the movie."
                                        },
                                        "reason": {
                                            "type": "string",
                                            "description": "The reason for recommending the movie in korean."
                                        }
                                    },
                                    "required": ["title", "release_date", "reason"],
                                    "additionalProperties": False
                                }
                            },
                            "dalle_prompt": {
                                "type": "string",
                                "description": "The prompt for generating an image using DALL.E3 in english."
                            }
                        },
                        "required": ["analysis", "movie_recommendations", "dalle_prompt"],
                        "additionalProperties": False
                    }
                }
            }
        )

        response_content = response.choices[0].message.content
        try:
            parsed_content = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f'JSON 파싱 중 오류 발생 : {e}')
        
        random_recommend = [(11, '광선검이 멋져요'), (13, '불가능에 대한 고찰'), (105, '유쾌함에 취하고 싶다')]
        idx = 0

        analysis = json.loads(response_content)["analysis"]
        movie_recommend = json.loads(response_content)["movie_recommendations"]
        made_prompt = json.loads(response_content)["dalle_prompt"]

        # dall.e에 사용할 프롬프트 저장
        self.dalle_prompt = made_prompt

        # recommended 객체 생성
        for recommend in movie_recommend:
            movie = Movie.objects.filter(title=recommend['title'])
            if movie:
                reason = recommend['reason']
            else:
                movie = Movie.objects.filter(tmdb_id= random_recommend[idx][0])
                reason = random_recommend[idx][1]
                idx += 1
            
            recommended = Recommended(movie=movie[0], movie_journal=self.movie_journal, reason=reason)
            recommended.save()


    def create_ai_img(self):
        """
        DALL.E3를 이용해 그림 생성
        """
        client = OpenAI(api_key=self.OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt= self.dalle_prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )

        ai_image_url = response.data[0].url
        self.movie_journal.ai_img = ai_image_url
        self.movie_journal.save()               # 수정사항 저장


    # 로그인한 사용자의 다이어리 목록 반환
    @action(detail=False, methods=["GET"], url_path='(?P<user_pk>[^/.]+)/list')
    # detail=False는 단일 객체가 아닌, 목록 조회용 메서드임을 나타냄
    def user_journals(self, request, user_pk=None):
        if user_pk:
            journals = self.queryset.filter(user_id=user_pk)
        else:
            journals = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(journals, many=True)
        return Response(serializer.data)

    # ModelViewSet에서 destroy(delete) 메서드가 기본 제공되므로 오버라이드할 필요 없음
    # 특정 다이어리(journal)를 삭제함
    # @action(detail=True, method=['DELETE'], url_path='delete')
    # def delete_journal(self, request, pk=None):
    #     journal = self.get_object()
    #     journal.delete()
    #     return Response({'message': 'Journal deleted'}, status=status.HTTP_204_NO_CONTENT)