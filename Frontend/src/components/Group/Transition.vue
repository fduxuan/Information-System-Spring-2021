<!--
   Created on 2021/5/14 3:31 下午

   @Author: fduxuan

   Desc:  过渡
 */
 -->
<template>
    <div  style="height: 100%; background: radial-gradient(#607d8b 15%, #000000 100%);box-sizing: border-box;">
      <a-progress
          :strokeWidth="16"
          :stroke-color="{
        '0%': '#108ee9',
        '100%': '#87d068',
      }" :percent="process_percent"  style="width: 40%; margin-top: 30px; margin-bottom: 10px"/>
      <br>
      <span style="font-weight: bold; color:#fff; font-size:120%">请耐心等待 ......</span>
      <div class="click">

        <input type="checkbox" class="switcher" checked="checked">
        <div class="glassball">
          <div class="electrode"></div>
          <div class="rays">
            <div class="ray">
              <span></span><span></span><span></span>
            </div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
          </div>
          <div class="rays">
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
          </div>
          <div class="rays">
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
          </div>
          <div class="rays">
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray bigwave"><span></span><span></span></div>
          </div>
          <div class="rays">
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
          </div>
          <div class="rays">
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
            <div class="ray"><span></span><span></span><span></span></div>
          </div>

        </div>
        <div class="base">
          <div></div>
          <div></div><span></span>
        </div>
        <div class="switch"></div>
      </div>

    </div>

</template>

<script>
export default {
    name: "Transition",
    components:{

    },

    data(){
        return{
          process_percent: 20
        }
    },


    methods:{

    },

    mounted(){
      let that = this
      const timer = setInterval(() =>{
        if (that.process_percent > 92){
          that.process_percent = 99.9
        }
        else{that.process_percent += 8}

        // 某些定时器操作
      }, 100);
        // 通过$once来监听定时器
        // 在beforeDestroy钩子触发时清除定时器
      if (this.process_percent>=99){
        clearInterval(timer);
      }

      this.$once('hook:beforeDestroy', () => {
        clearInterval(timer);
      })

    },

}
</script>

<style scoped>
>>> .ant-progress-text{
  color: #ffffff;
  font-weight: bold;
}
.click {
  position: relative;
  margin: 0 auto;
  width: 350px;
  height: 350px;
  top: 4vh;
}
.base {
  position: absolute;
  background: #222;
  width: 300px;
  height: 200px;
  margin: 3em auto;
  z-index: 0;
  top: 286px;
  left: 25px;
}
.base:before {
  position: absolute;
  top: -44px;
  width: 300px;
  height: 5em;
  border-radius: 100%;
  content: "";
  background: radial-gradient(#222 20%, #353535);
  background: conic-gradient(from 167deg, #666666, #232323, #232323, #666666);
  border: 2px solid #597481;
  box-sizing: border-box;
  left: 0;
  z-index: 0;
}
.base:after {
  position: absolute;
  left: -35px;
  bottom: -65px;
  width: 370px;
  height: 110px;
  border-radius: 30% 30% 50% 50%;
  content: "";
  background: #222222;
  z-index: -1;
}
.base div {
  background: #222222;
  height: 100px;
  margin-top: 3em;
  float: left;
  margin-left: -53px;
  width: 63%;
  transform: rotate(-85deg);
  z-index: -1;
  position: relative;
}
.base div + div {
  margin-top: -99px;
  margin-left: 164px;
  transform: rotate(85deg);
}
.base span {
  position: absolute;
  left: -51px;
  bottom: -4px;
  width: 402px;
  height: 160px;
  border-radius: 0% 0% 80% 80%;
  content: "";
  background: #242f3400;
  z-index: 0;
  border: 2px solid transparent;
  border-bottom-color: #435761;
}
input.switcher {
  width: 48px;
  height: 48px;
  opacity: 0;
  position: absolute;
  z-index: 3333;
  margin: 0;
  cursor: pointer;
  outline: none;
  border-radius: 50px !important;
  top: 425px;
  left: 151px;
}
.glassball {
  position: relative;
  overflow: hidden;
  margin: 0 auto;
  width: 100%;
  height: 100%;
  border-radius: 100%;
  /*background-color: rgb(255 255 255/ 0.15);*/
  top: 0;
  box-shadow: 0 20px 30px rgba(0, 0, 0, 0.2),
  inset 0 10px 30px 5px rgba(255, 255, 255, 1);
  z-index: 2
}
.glassball:after {
  background: radial-gradient(
      ellipse at center,
      rgba(255, 255, 255, 0.5) 0%,
      rgba(255, 255, 255, 0) 70%
  );
  border-radius: 50%;
  /*box-shadow: inset 0 20px 30px rgb(255 255 255 / 30%);*/
  content: "";
  height: 96%;
  left: 2%;
  position: absolute;
  width: 96%;
  top: 2%;
  z-index: 1;
}
.glassball:hover {
  cursor: grab;
}
.glassball:before {
  position: absolute;
  left: 48%;
  top: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle closest-side, #9c27b0, transparent);
  transform: translate(-45%, -48%);
  transition: width 0.2s ease, height 0.2s ease;
  animation: spark 5ms ease 0s infinite alternate;
  border: 8px dotted #24e6ff;
  filter: blur(15px);
  border-radius: 100%;
  z-index: 2;
  font-size: 10em;
  color: #d6faff;
  text-align: center;
  line-height: 1;
  content: "s";
  display: none;
  opacity: 0.75;
}
.glassball:hover:before {
  width: 120px;
  height: 150px;
}
input.switcher:checked + .glassball:before,
input.switcher:checked + .glassball:after {
  display: block;
}
input.switcher:checked + .glassball:after {
  width: 97%;
  height: 97%;
  left: 1.5%;
  top: 1.5%;
}
input.switcher:checked + .glassball:hover:after {
  animation: rotation 3s ease 0s infinite alternate;
  background: radial-gradient(
      ellipse at center,
      #ffffff7d 0%,
      #54ecff94 10%,
      transparent 100%
  );
  filter: brightness(1.75);
  opacity: 0.5;
}
input.switcher:checked + .glassball {
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
  background: radial-gradient(
      circle,
      #ff5affb8 0%,
      #ff5affb8 20%,
      #5493d2a8 70%,
      #5493d2a8 100%
  );
  animation: innerlight 5s linear 0s infinite,
  shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transition: background 0.4s ease 0s;
  box-shadow: 0 0 15px 5px #5493d2a8;
  border: 1px solid transparent;
}

.switch {
  background: #1b1b1b;
  width: 37px;
  height: 37px;
  position: absolute;
  margin-left: calc(50% - 19px);
  top: 430px;
  border: 3px solid #4e4e4e;
  z-index: 5;
  font-size: 0.75em;
  border-radius: 100%;
  box-shadow: 0 0 10px 0 #000000, 0 0 5px 1px #2d2d2d, 0 0 3px 1px #000 inset;
}
.switch::before {
  content: "";
  position: absolute;
  width: 13px;
  height: 13px;
  bottom: 6px;
  border: 3px solid #4e4e4e;
  border-top-color: transparent;
  border-radius: 100%;
  left: 6px;
}
.switch::after {
  content: "";
  position: absolute;
  width: 3px;
  height: 9px;
  bottom: 16px;
  left: 14px;
  background: #4e4e4e;
}
input:checked + div + div + .switch {
  background: linear-gradient(to bottom, #171717, #404040);
  color: #fff;
  box-shadow: 0 0 10px 0 #03a9f4, 0 0 5px 1px #03a9f4;
  border-color: #222222d1;
}
input:checked + div + div + .switch:before {
  border-color: transparent #03a9f4 #03a9f4 #03a9f4;
}
input:checked + div + div + .switch:after {
  background: #03a9f4;
}
.electrode {
  background: linear-gradient(75deg, #3a3a3a 20%, #2d2d2d);
  width: 1em;
  height: 8.75em;
  bottom: 1.25em;
  position: absolute;
  left: calc(50% - 0.5em);
  overflow: visible;
  border-bottom: 1px solid #657882;
  border-radius: 0 0 6px 5px;
}
.electrode:before {
  position: absolute;
  left: -16px;
  top: -40px;
  width: 3em;
  height: 3em;
  border-radius: 100%;
  content: "";
  background: radial-gradient(at top left, #4a4949 20%, #2d2d2d);
  border: 1px solid #758e99;
  box-sizing: border-box;
}
.electrode:after {
  position: absolute;
  left: -3px;
  bottom: -11px;
  width: 1.375em;
  height: 1em;
  border-radius: 140px/50px;
  content: "";
  background: linear-gradient(-263deg, #191919 20%, #0a0a0a);
  z-index: -1;
}
input.switcher:checked + .glassball .electrode:after {
  background: linear-gradient(-263deg, #3a3a3a 20%, #2d2d2d);
}
input.switcher:checked + .glassball .electrode:before {
  background: radial-gradient(
      ellipse farthest-corner at 30px 30px,
      #999,
      #e449ff,
      #e449ff,
      #9763ff,
      #62edff,
      #fff
  );
  box-shadow: 0 0 10px 2px #e449ffb3, 0 0 10px 2px #fff,
  0 0 50px -10px #fff inset;
  border-color: #ffffff94;
}
input.switcher + .glassball .rays {
  display: none;
}
input.switcher:checked + .glassball .rays {
  display: block;
  float: left;
  width: 100%;
  height: 100%;
  position: absolute;
}
.ray {
  width: 10em;
  height: 2em;
  position: absolute;
  bottom: 9em;
  filter: drop-shadow(0px 0px 7px #9660f7) drop-shadow(0px 0px 2px #fff);
}
.ray:before {
  content: "";
  width: 0.5em;
  height: 0.45em;
  border: 2px dashed #03a9f4;
  position: absolute;
  border-width: 3px 3px 1px 1px;
  transform: rotate(87deg);
  top: 0.3em;
  left: 3px;
  border-radius: 10px 5px 8px 7px;
  filter: blur(2px);
  box-shadow: 0 0 10px -1px black;
}
.ray:after {
  content: "s";
  float: left;
  width: 0.5em;
  height: 1.5em;
  margin-top: 20px;
  margin-left: 0px;
  animation: blink 1s linear 0s infinite alternate;
  background: radial-gradient(circle closest-side, #9c27b0, transparent);
  transform: translate(-45%, -48%);
  transition: width 0.2s ease, height 0.2s ease;
  border: 8px dotted #24e6ff;
  filter: blur(5px);
  border-radius: 100%;
  z-index: 2;
  font-size: 4em;
  color: #d6faff;
  text-align: center;
  line-height: 1;
}
.ray span {
  width: 4em;
  height: 1em;
  border: solid 0.25em #000;
  border-radius: 238%/50px 50px 0 0;
  position: absolute;
  top: 0.5em;
  left: 0;
  border-color: #6bbdff transparent transparent transparent;
}

.ray span + span {
  left: 30%;
  transform: rotate(180deg);
  top: 0.15em;
}
.ray span + span + span {
  left: 60%;
  transform: rotate(0deg);
  top: 0.5em;
}

.ray span:last-of-type:before {
  content: "";
  float: right;
  width: 8px;
  height: 8px;
  background: #d1eefb;
  border-radius: 100%;
  box-shadow: 0 0 4px 3px #fff;
  filter: blur(1px);
  margin-top: -2px;
  left: 3px;
  position: relative;
}
.ray.bigwave span:last-of-type:before {
  content: "";
  float: left;
  width: 8px;
  height: 8px;
  background: #d1eefb;
  border-radius: 100%;
  box-shadow: 0 0 4px 3px #fff;
  filter: blur(1px);
  margin-top: -3px;
  left: -2px;
  position: relative;
}
.ray.bigwave span {
  width: 55%;
  border-width: 4px;
}
.ray.bigwave span + span {
  width: 60%;
  left: 40%;
  border-width: 5px;
  margin-left: 4px;
  margin-top: 2px;
}

.rays + .rays {
  transform: rotate(180deg);
}
.rays + .rays + .rays {
  transform: rotate(90deg);
}
.rays + .rays + .rays + .rays {
  transform: rotate(270deg);
}
.rays + .rays + .rays + .rays + .rays {
  transform: skew(-187deg, 0deg) scale(0.675) rotate(0deg);
  display: none;
  animation: touchray1 2.5s ease 0.1s infinite alternate;
}
.rays + .rays + .rays + .rays + .rays + .rays {
  transform: skew(-140deg, -40deg) scale(0.675) rotate(180deg);
  display: none;
  animation: touchray2 1s ease 0.25s infinite;
}
input.switcher:checked
+ .glassball:hover
.rays
+ .rays
+ .rays
+ .rays
+ .rays {
  display: block;
}

.rays + .rays + .rays + .rays + .rays .ray {
  width: 8.5em;
  animation: ray1 0.5s linear 0s infinite alternate;
}
.rays + .rays + .rays + .rays + .rays .ray span {
  border-top-width: 8px;
}

.ray:nth-of-type(1) {
  animation: ray1 0.5s linear 0s infinite;
}
.ray:nth-of-type(2) {
  animation: ray1 0.75s linear 0s infinite alternate;
}
.ray:nth-of-type(3) {
  animation: ray1 0.65s linear 0s infinite reverse;
}
.ray:nth-of-type(4) {
  animation: ray1 0.95s linear 0s infinite alternate;
}
.ray:nth-of-type(5) {
  animation: ray1 0.85s linear 0s infinite reverse;
}

.rays + .rays .ray:nth-of-type(1) {
  animation-duration: 1.55s;
}
.rays + .rays .ray:nth-of-type(2) {
  animation-duration: 1.75s;
}
.rays + .rays .ray:nth-of-type(3) {
  animation-duration: 0.65s;
}
.rays + .rays .ray:nth-of-type(4) {
  animation-duration: 1.85s;
}
.rays + .rays .ray:nth-of-type(5) {
  animation-duration: 1.6s;
}

.rays + .rays + .rays .ray:nth-of-type(1) {
  animation-duration: 1.15s;
}
.rays + .rays + .rays .ray:nth-of-type(2) {
  animation-duration: 1.5s;
}
.rays + .rays + .rays .ray:nth-of-type(3) {
  animation-duration: 1.35s;
}
.rays + .rays + .rays .ray:nth-of-type(4) {
  animation-duration: 1s;
}
.rays + .rays + .rays .ray:nth-of-type(5) {
  animation-duration: 1.25s;
}

.rays + .rays + .rays + .rays .ray:nth-of-type(1) {
  animation-duration: 1.05s;
}
.rays + .rays + .rays + .rays .ray:nth-of-type(2) {
  animation-duration: 1.35s;
}
.rays + .rays + .rays + .rays .ray:nth-of-type(3) {
  animation-duration: 1.25s;
}
.rays + .rays + .rays + .rays .ray:nth-of-type(4) {
  animation-duration: 1.15s;
}
.rays + .rays + .rays + .rays .ray:nth-of-type(5) {
  animation-duration: 1.45s;
}

.rays + .rays + .rays + .rays + .rays .ray:nth-of-type(1) {
  animation-duration: 0.85s;
}
.rays + .rays + .rays + .rays + .rays .ray:nth-of-type(2) {
  animation-duration: 0.95s;
}
.rays + .rays + .rays + .rays + .rays .ray:nth-of-type(3) {
  animation-duration: 0.75s;
}

.rays + .rays + .rays + .rays + .rays + .rays .ray:nth-of-type(1) {
  animation-duration: 1.1s;
}
.rays + .rays + .rays + .rays + .rays + .rays .ray:nth-of-type(2) {
  animation-duration: 1.25s;
}
.rays + .rays + .rays + .rays + .rays + .rays .ray:nth-of-type(3) {
  animation-duration: 1.35s;
}

@keyframes rotation {
  50% {
    transform: rotate(360deg);
  }
}
@keyframes blink {
  0% {
    background: radial-gradient(circle closest-side, #ff5affb8, #5493d2a8);
    transform: translate(-50%, -50%) scale(0.75) rotate(6deg);
  }
  50% {
    background: radial-gradient(circle closest-side, #5493d2a8, #ff5affb8);
    transform: translate(-50%, -50%) scale(0.5) rotate(2deg);
  }
  100% {
    background: radial-gradient(circle closest-side, #ffffffa8, #5493d2a8);
    transform: translate(-50%, -50%) scale(0.35) rotate(11deg);
  }
}
@keyframes innerlight {
  0% {
    background-size: 105% 105%;
    background-position: center center;
    box-shadow: 0 0 15px 5px #5493d2a8;
  }
  25% {
    box-shadow: 0 0 15px 5px #ff5aff30;
  }
  50% {
    background-size: 85% 85%;
    background-position: center center;
    box-shadow: 0 0 15px 5px #5493d2a8;
  }
  75% {
    box-shadow: 0 0 15px 5px #ff5aff30;
  }
  100% {
    background-size: 105% 105%;
    background-position: center center;
    box-shadow: 0 0 15px 5px #5493d2a8;
  }
}
@keyframes touchray1 {
  0% {
    transform: skew(-187deg, 0deg) scale(0.675) rotate(0deg);
  }
  50% {
    transform: skew(-185deg, 2deg) scale(0.525) rotate(180deg);
    opacity: 1;
  }
  51% {
    opacity: 0;
  }
  52% {
    opacity: 1;
  }
  100% {
    transform: skew(-188deg, -2deg) scale(0.625) rotate(360deg);
  }
}
@keyframes touchray2 {
  0% {
    transform: skew(-140deg, -40deg) scale(0.675) rotate(140deg);
  }
  50% {
    transform: skew(-143deg, -42deg) scale(0.525) rotate(0deg);
    opacity: 1;
  }
  51% {
    opacity: 0;
  }
  52% {
    opacity: 1;
  }
  100% {
    transform: skew(-145deg, -38deg) scale(0.625) rotate(210deg);
  }
}
@keyframes spark {
  0% {
    background: radial-gradient(circle closest-side, #ff5affb8, #5493d2a8);
    transform: translate(-50%, -50%) scale(0.75) rotate(0deg);
  }
  50% {
    background: radial-gradient(circle closest-side, #5493d2a8, #ff5affb8);
    transform: translate(-50%, -50%) scale(0.5) rotate(180deg);
  }
  100% {
    background: radial-gradient(circle closest-side, #ffffffa8, #5493d2a8);
    transform: translate(-50%, -50%) scale(1) rotate(360deg);
  }
}
@keyframes ray1 {
  0% {
    opacity: 0;
    transform: rotate(0deg) translate(0px, 0px);
  }
  12% {
    opacity: 1;
    transform: rotate(22deg) translate(0px, -35px);
    filter: brightness(1.75);
  }
  25% {
    opacity: 0;
    transform: rotate(45deg) translate(-33px, -69px);
  }
  37% {
    opacity: 1;
    transform: rotate(67deg) translate(-64px, -86px);
    filter: brightness(1.15);
  }
  50% {
    opacity: 0;
    transform: rotate(90deg) translate(-108px, -93px);
  }
  62% {
    opacity: 1;
    transform: rotate(112deg) translate(-140px, -90px);
    filter: brightness(1.25);
  }
  75% {
    opacity: 0;
    transform: rotate(135deg) translate(-169px, -69px);
  }
  87% {
    opacity: 1;
    transform: rotate(157deg) translate(-185px, -36px);
    filter: brightness(1.75);
  }
  100% {
    opacity: 0;
    transform: rotate(180deg) translate(-192px, 6px);
  }
}

</style>
