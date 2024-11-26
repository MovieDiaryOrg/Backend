<script setup>
import { RouterLink, RouterView,useRouter } from 'vue-router'
import { onMounted } from 'vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination, Navigation, Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

// 버튼 누르면 메인페이지로
const router = useRouter()
function goToHomePage() {
  router.push('main/') 
}
// aos
onMounted(() => {
  AOS.init({
    duration: 800,
    offset: 0
  })
})

// Swiper 설정
const swiperOptions = {
  modules: [Pagination, Navigation, Autoplay],
  slidesPerView: 1,
  spaceBetween: 0,
  loop: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  pagination: {
    clickable: true,
  },
  navigation: true,
}
</script>

<template>
<link rel="stylesheet" href="src/assets/css/styles.css">
    <link rel="stylesheet" href="src/assets/css/vendor.css">
<div>
   <!-- preloader
    ================================================== -->
    <div id="preloader">
        <div id="loader" class="dots-fade">
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>


  <header class="s-header">

  <div class="s-header__logo">
      <a href="index.html">
          <img src="@/assets/images/logo.svg" alt="Homepage">
      </a>
  </div>

  <div class="s-header__content">

      <nav class="s-header__nav-wrap">
          <ul class="s-header__nav">
              <li><a class="smoothscroll" href="#hero" title="Intro">Home</a></li>
              <li><a class="smoothscroll" href="#about" title="About">About</a></li>
              <li><a class="smoothscroll" href="#portfolio" title="Works">reviews</a></li>
              <li><a class="smoothscroll" href="#portfolio" title="Works">start</a></li>
          </ul>
      </nav> <!-- end s-header__nav-wrap -->

      <a href="login.html" class="btn btn--primary btn--small">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 0l-6 22-8.129-7.239 7.802-8.234-10.458 7.227-7.215-1.754 24-12zm-15 16.668v7.332l3.258-4.431-3.258-2.901z"/></svg>
          Join us
      </a>

  </div> <!-- end header-content -->

  <a class="s-header__menu-toggle" href="#0"><span>Menu</span></a>

  </header> <!-- end s-header -->

  <!-- hero
  ================================================== -->
  <section id="hero" class="s-hero target-section">

  <div class="s-hero__bg">
      <div class="gradient-overlay"></div>
  </div>

  <div class="row s-hero__content">
      <div class="column">

          <h1>Film.e</h1>
          <div class="s-hero__content-about">

              <p>
                  Your cinematic journey <br>
                  beautifully recorded.
              </p>

          </div>

      </div>
  </div>

  <div class="s-hero__video">
      <a class="s-hero__video-link" href="https://player.vimeo.com/video/117310401?color=01aef0&amp;title=0&amp;byline=0&amp;portrait=0" data-lity="">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21 12l-18 12v-24z"/></svg>
          <span class="s-hero__video-text">Play Video</span>
      </a>
  </div>

  <div class="s-hero__scroll">
      <a href="#about" class="s-hero__scroll-link smoothscroll">
          Scroll Down
      </a>
  </div>

  </section> <!-- end s-hero -->


  <!-- about
  ================================================== -->
  <section id="about" class="s-about">
  <div class="horizontal-line"></div>
  <div class="row">
      <div class="column large-12">
          <div class="section-title" data-num="01" data-aos="fade-up">
              <h3 class="h6">About</h3>
          </div>

      </div>

      <div class="column large-6 w-900-stack s-about__intro-text">
          <h1 class="display-1" data-aos="fade-up">
              영화의 감정을 예술로 기록하고, 당신의 감성에 맞춘 특별한 추천을 만나보세요.
          </h1>

          <p class="lead" data-aos="fade-up">
              우리의 서비스는 다양한 플랫폼에서 관람한 영화를 하나의 공간에 기록하고, 감상평을 기반으로 AI가 특별한 그림일기를 만들어 줍니다. 또한, 감정 분석을 통해 맞춤형 영화 추천을 제공하며, 다른 사람들의 감상문과 소통할 수 있는 커뮤니티를 제공합니다.

          </p>
      </div>

      <div class="column large-6 w-900-stack s-about__photo-block">
          <div class="s-about__photo" data-aos="fade-up"></div>
      </div>
  </div>

  <div class="row block-large-1-2 block-tab-full s-about__process item-list">
      <div class="column item item-process" data-aos="fade-up">
          <h3 class="item-title">통합 영화 기록</h3>
          <p>
              여러 플랫폼에서 본 영화들을 한 곳에 모아 쉽게 관리할 수 있는 기록 서비스입니다. 관람 일시와 장소까지 한눈에 정리하세요.

          </p>
      </div>
      <div class="column item item-process" data-aos="fade-up">
          <h3 class="item-title">AI 그림일기 생성</h3>
          <p> 영화 감상평을 AI가 분석해 감정과 주요 키워드를 추출하고, 이를 바탕으로 예술적인 그림일기를 만들어 드립니다.</p>
      </div>
      <div class="column item item-process" data-aos="fade-up">
          <h3 class="item-title">감상평 기반 맞춤형 추천</h3>
          <p>
              감상평을 분석해 감정선에 어울리는 영화를 추천합니다. 긍정적 경험은 비슷한 감정을, 부족했던 점은 개선된 작품을 제안합니다. </p>
      </div>
      <div class="column item item-process" data-aos="fade-up">
          <h3 class="item-title">영화 감상 커뮤니티</h3>
          <p>
              다른 사람들의 감상문을 읽고 소통할 수 있는 커뮤니티를 제공합니다. 영화에 대한 다양한 시각과 감상을 함께 나눠보세요.</p>
      </div>
  </div>

  </section> <!-- end s-about -->

  <section id="reviews" class="s-portfolio">
    <div class="row s-porfolio__top">
        <div class="column large-12 text-center">
            <div class="section-title" data-num="02" data-aos="fade-up">
                <h3 class="h6">REVIEWS</h3>
            </div>
        </div>
        <div class="column large-12 text-center">
            <h2 class="display-1" data-aos="fade-up">
                영화 애호가들이 직접 경험한 특별한 순간들!
            </h2>
        </div>
    </div>
    <div class="row testimonials">
        <div class="column large-12">
            <swiper
                :modules="swiperOptions.modules"
                :slides-per-view="swiperOptions.slidesPerView"
                :space-between="swiperOptions.spaceBetween"
                :loop="swiperOptions.loop"
                :autoplay="swiperOptions.autoplay"
                :pagination="swiperOptions.pagination"
                :navigation="swiperOptions.navigation"
                class="testimonial-slider"
                data-aos="fade-up"
            >
                <!-- 슬라이드 항목들 -->
                <swiper-slide class="testimonial-slider__slide">
                    <p>
                        “영화 기록을 한 곳에서 관리할 수 있어 정말 편리해요! 각 플랫폼에서 본 영화를 기억할 필요 없고, 일기처럼 감상평을 정리할 수 있어 더 의미 있어졌요. 영화 애호가들에게 딱 맞는 서비스입니다!”
                    </p>
                    <div class="testimonial-slider__author">
                        <img src="@/assets/images/avatars/user-02.jpg" alt="Author image" class="testimonial-slider__avatar">
                        <cite class="testimonial-slider__cite">
                            <strong>Tim Cook</strong>
                            <span>CEO, Apple</span>
                        </cite>
                    </div>
                </swiper-slide>
                <swiper-slide class="testimonial-slider__slide">
                    <p>
                        “AI 그림일기는 정말 독특하고 창의적이에요! 제 감상평이 예술 작품으로 변신하니 감상이 더 특별하게 느껴졌어요. SNS에 공유했더니 친구들도 정말 신기해하더군요.”
                    </p>
                    <div class="testimonial-slider__author">
                        <img src="@/assets/images/avatars/user-01.jpg" alt="Author image" class="testimonial-slider__avatar">
                        <cite class="testimonial-slider__cite">
                            <strong>Sundar Pichai</strong>
                            <span>CEO, Google</span>
                        </cite>
                    </div>
                </swiper-slide>
                <swiper-slide class="testimonial-slider__slide">
                    <p>
                        “단순한 장르 추천과는 차원이 다릅니다! 제가 좋아하는 감정을 기반으로 한 영화들이 추천되어 정말 만족스럽게 감상했어요. 감성적 울림이 있는 영화를 찾고 싶을 때 아주 유용해요.”
                    </p>
                    <div class="testimonial-slider__author">
                        <img src="@/assets/images/avatars/user-04.jpg" alt="Author image" class="testimonial-slider__avatar">
                        <cite class="testimonial-slider__cite">
                            <strong>Satya Nadella</strong>
                            <span>CEO, Microsoft</span>
                        </cite>
                    </div>
                </swiper-slide>
                <swiper-slide class="testimonial-slider__slide">
                    <p>
                        “감상평을 분석해 감정에 맞춘 영화를 추천해준다는 점이 너무 신선해요! 감정 상태에 따라 영화를 선택할 수 있어서 기분에 딱 맞는 작품을 감상할 수 있었어요. 매번 새로운 발견이 즐겁습니다!”
                    </p>
                    <div class="testimonial-slider__author">
                        <img src="@/assets/images/avatars/user-05.jpg" alt="Author image" class="testimonial-slider__avatar">
                        <cite class="testimonial-slider__cite">
                            <strong>Jeff Bezos</strong>
                            <span>CEO, Amazon</span>
                        </cite>
                    </div>
                </swiper-slide>
            </swiper>
        </div>
    </div>
</section>

  <section id="portfolio" class="s-portfolio">
    <div class="row s-porfolio__top">
        <div class="column large-6 w-900-stack">
            <div class="section-title" data-num="03" data-aos="fade-up">
                <h3 class="h6">START</h3>
            </div>
        </div>
        <div class="column large-6 w-900-stack">
            <h1 class="display-1" data-aos="fade-up">
                Here are some of our projects we done lately. Feel
                free to check them out.
            </h1>
        </div>
    </div> <!-- end s-portfolio__top-->

    <div class="row s-portfolio__list block-large-1-2 block-tab-full collapse">
        <div class="column" data-aos="fade-up">
            <div class="folio-item">
                <div class="folio-item__thumb">
                    <a class="folio-item__thumb-link" href="@/assets/images/portfolio/gallery/g-red-wheel.jpg" title="The Red Wheel" data-size="1050x700">
                        <img src="@/assets/images/portfolio/red-wheel.jpg" 
                            srcset="@/assets/images/portfolio/red-wheel.jpg 1x, @/assets/images/portfolio/red-wheel@2x.jpg 2x" alt="">
                    </a>
                </div>
                <div class="folio-item__info">
                    <div class="folio-item__cat">Branding</div>
                    <h4 class="folio-item__title">The Red Wheel</h4>
                </div>
                <a href="https://www.behance.net/" title="Project Link" class="folio-item__project-link">Project Link</a>
                <div class="folio-item__caption">
                    <p>Vero molestiae sed aut natus excepturi. Et tempora numquam. Temporibus iusto quo.Unde dolorem corrupti neque nisi.</p>
                </div>
            </div>
        </div> <!-- end column -->
        <div class="column" data-aos="fade-up">
            <div class="folio-item">
                <div class="folio-item__thumb">
                    <a class="folio-item__thumb-link" href="@/assets/images/portfolio/gallery/g-music-life.jpg" title="Music Life" data-size="1050x700">
                        <img src="@/assets/images/portfolio/music-life.jpg" 
                            srcset="@/assets/images/portfolio/music-life.jpg 1x, @/assets/images/portfolio/music-life@2x.jpg 2x" alt="">
                    </a>
                </div>
                <div class="folio-item__info">
                    <div class="folio-item__cat">Frontend Design</div>
                    <h4 class="folio-item__title">Music Life</h4>
                </div>
                <a href="https://www.behance.net/" title="Project Link" class="folio-item__project-link">Project Link</a>
                <div class="folio-item__caption">
                    <p>Vero molestiae sed aut natus excepturi. Et tempora numquam. Temporibus iusto quo.Unde dolorem corrupti neque nisi.</p>
                </div>
            </div>
        </div> <!-- end column -->
        <div class="column" data-aos="fade-up">
            <div class="folio-item">
                <div class="folio-item__thumb">
                    <a class="folio-item__thumb-link" href="@/assets/images/portfolio/gallery/g-oi-logo.jpg" Title="OI Logo" data-size="1050x700">
                        <img src="@/assets/images/portfolio/oi-logo.jpg" 
                            srcset="@/assets/images/portfolio/oi-logo.jpg 1x, @/assets/images/portfolio/oi-logo@2x.jpg 2x" alt="">
                    </a>
                </div>
                <div class="folio-item__info">
                    <div class="folio-item__cat">Branding</div>
                    <h4 class="folio-item__title">OI Logo</h4>
                </div>
                <a href="https://www.behance.net/" title="Project Link" class="folio-item__project-link">Project Link</a>
                <div class="folio-item__caption">
                    <p>Vero molestiae sed aut natus excepturi. Et tempora numquam. Temporibus iusto quo.Unde dolorem corrupti neque nisi.</p>
                </div>
            </div>
        </div> <!-- end column -->
        <div class="column" data-aos="fade-up">
            <div class="folio-item">
                <div class="folio-item__thumb">
                    <a class="folio-item__thumb-link" href="@/assets/images/portfolio/gallery/g-corrugated-sheets.jpg" title="Corrugated Sheets" data-size="1050x700">
                        <img src="@/assets/images/portfolio/corrugated-sheets.jpg" 
                            srcset="@/assets/images/portfolio/corrugated-sheets.jpg 1x, @/assets/images/portfolio/corrugated-sheets@2x.jpg 2x" alt="">
                    </a>
                </div>
                <div class="folio-item__info">
                    <div class="folio-item__cat">Frontend Design</div>
                    <h4 class="folio-item__title">Corrugated Sheets</h4>
                </div>
                <a href="https://www.behance.net/" title="Project Link" class="folio-item__project-link">Project Link</a>
                <div class="folio-item__caption">
                    <p>Vero molestiae sed aut natus excepturi. Et tempora numquam. Temporibus iusto quo.Unde dolorem corrupti neque nisi.</p>
                </div>
            </div>
        </div> <!-- end column -->
    </div> <!-- folio-list -->
    <div class="row">
        <div class="column large-12 text-center" data-aos="fade-up">
            <h2 class="display-2 mb-4">
                지금 바로 시작해보세요
            </h2>
            <div class="start-button-container" style="margin-top: 3rem;">
                <img 
                id="startButton" 
                src="@/assets/images/start_button.png" 
                alt="시작하기" 
                style="cursor: pointer; max-width: 200px;"
                @click="goToHomePage"
                >
            </div>
        </div>
    </div>

  </section> <!-- end s-portfolio -->




 

  <!-- photoswipe background
  ================================================== -->
  <div aria-hidden="true" class="pswp" role="dialog" tabindex="-1">

  <div class="pswp__bg"></div>
  <div class="pswp__scroll-wrap">

      <div class="pswp__container">
          <div class="pswp__item"></div>
          <div class="pswp__item"></div>
          <div class="pswp__item"></div>
      </div>

      <div class="pswp__ui pswp__ui--hidden">
          <div class="pswp__top-bar">
              <div class="pswp__counter"></div><button class="pswp__button pswp__button--close" title="Close (Esc)"></button> <button class="pswp__button pswp__button--share" title=
              "Share"></button> <button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button> <button class="pswp__button pswp__button--zoom" title=
              "Zoom in/out"></button>
              <div class="pswp__preloader">
                  <div class="pswp__preloader__icn">
                      <div class="pswp__preloader__cut">
                          <div class="pswp__preloader__donut"></div>
                      </div>
                  </div>
              </div>
          </div>
          <div class="pswp__share-modal pswp__share-modal--hidden pswp__single-tap">
              <div class="pswp__share-tooltip"></div>
          </div><button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)"></button> <button class="pswp__button pswp__button--arrow--right" title=
          "Next (arrow right)"></button>
          <div class="pswp__caption">
              <div class="pswp__caption__center"></div>
          </div>
      </div>

  </div>

  </div> <!-- end photoSwipe background -->
</div><!-- end of template-->
</template>

<style scoped>
/* 필요한 스타일 파일들 import 되어 있는지 확인 */
@import '@/assets/css/vendor.css';
@import '@/assets/css/styles.css';

.no-break {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 모바일 화면에서는 줄바꿈 허용 */
@media screen and (max-width: 600px) {
  .no-break {
    white-space: normal;
  }
}

/* Swiper 커스텀 스타일 */
:deep(.swiper-pagination-bullet) {
  background: #ffffff;
  opacity: 0.5;
}

:deep(.swiper-pagination-bullet-active) {
  opacity: 1;
}

:deep(.swiper-button-prev),
:deep(.swiper-button-next) {
  color: #ffffff;
}

.testimonial-slider {
  position: relative;
  width: 100%;
  height: auto; /* 높이 자동 조정 */
  padding-bottom: 40px;
  overflow: visible; /* 잘리지 않도록 설정 */
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
}

/* 슬라이드 스타일 */
.testimonial-slider__slide {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 수직 중앙 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  padding: 2rem;
  min-height: 400px; /* 최소 높이 설정 */
  box-sizing: border-box;
}

/* 텍스트 컨테이너 스타일 */
.testimonial-slider__slide p {
  font-size: 2.5rem; /* 5배로 키움 */
  line-height: 1.8;
  margin: 0 auto; /* 중앙 정렬 */
  max-width: 80%; /* 최대 너비 제한 */
  word-break: break-word; /* 긴 텍스트 줄바꿈 */
  white-space: normal; /* 텍스트 줄바꿈 허용 */
}

/* 저자 정보 스타일 */
.testimonial-slider__author {
  margin-top: 2rem; /* 텍스트와 간격 추가 */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.testimonial-slider__avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.testimonial-slider__cite {
  text-align: left;
  font-size: 2rem; /* 저자 정보 글씨 크기 증가 */
}

/* 반응형 스타일 */
@media screen and (max-width: 768px) {
  .testimonial-slider__slide {
    padding: 1rem;
    min-height: auto; /* 최소 높이 해제 */
  }

  .testimonial-slider__slide p {
    font-size: 4rem; /* 모바일에서 글씨 크기 줄임 */
    line-height: 1.6;
  }

  .testimonial-slider__cite {
    font-size: 1.5rem; /* 저자 정보도 줄임 */
  }
}

/* 추가 수정: 전체 정렬 보정 */
.testimonial-slider__slide p {
  display: block;
  margin: 0 auto; /* 수평 중앙 정렬 */
  text-align: center;
}

/* Swiper 네비게이션 버튼 위치 조정 */
:deep(.swiper-button-prev),
:deep(.swiper-button-next) {
  top: 50%;
  transform: translateY(-50%);
}

:deep(.swiper-button-prev) {
  left: 10px;
}

:deep(.swiper-button-next) {
  right: 10px;
}

/* 반응형 스타일 */
@media screen and (max-width: 768px) {
  .testimonial-slider__slide {
    padding: 1rem;
    min-height: auto; /* 최소 높이 해제 */
  }

  .testimonial-slider__slide p {
    font-size: 1rem;
    line-height: 1.6;
  }
}

/* 슬라이드 전환 효과 개선 */
:deep(.swiper-slide) {
  opacity: 0;
  transition: opacity 0.3s ease;
}

:deep(.swiper-slide-active) {
  opacity: 1;
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .testimonial-slider__slide {
    padding: 2rem;
  }
  
  .testimonial-slider__slide p {
    font-size: 1.4rem;
  }
}

/* 추가 수정: 잘리지 않도록 설정 */
.testimonial-slider__slide {
  overflow: visible; /* 슬라이드 내부 내용이 잘리지 않도록 */
}

.swiper {
  overflow: visible; /* 부모 컨테이너도 잘림 방지 */
}
</style>
