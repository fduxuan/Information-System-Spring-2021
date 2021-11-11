<!--
   Created on 2021/5/30 4:10 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
  <a-modal
      :visible="visible"
      title="修改头像"
      :maskClosable="false"
      :confirmLoading="confirmLoading"
      :width="1000"
      @cancel="cancelHandel">
    <a-row>
      <a-col :xs="24" :md="12" :style="{height: '350px'}">
        <vue-cropper
            ref="cropper"
            :img="options.img"
            :info="true"
            :autoCrop="options.autoCrop"
            :autoCropWidth="options.autoCropWidth"
            :autoCropHeight="options.autoCropHeight"
            :fixedBox="options.fixedBox"
            @realTime="realTime"
        >
        </vue-cropper>
      </a-col>
      <a-col :xs="24" :md="12" :style="{height: '350px'}">
        <div class="avatar-upload-preview">
          <img :src="previews.url" :style="previews.img"/>
        </div>
      </a-col>
    </a-row>
    <template slot="footer">
      <a-button key="back" @click="cancelHandel">取消</a-button>
      <a-button key="submit" type="primary" :loading="confirmLoading" @click="okHandel">保存</a-button>
    </template>
  </a-modal>
</template>

<script>
import { VueCropper } from 'vue-cropper'
export default {
    name: "CropperModal",
    components:{
      VueCropper
    },
    data(){
        return{
          visible: false,
          img: null,
          confirmLoading: false,

          options: {
            img: undefined,//裁剪图片的地址
            autoCrop: true, //是否默认生成截图框
            autoCropWidth: 300, //默认生成截图框宽度
            autoCropHeight: 300, //默认生成截图框高度
            fixedBox: true //固定截图框大小 不允许改变
          },
          previews: {},
          url:{
            upload:'/sys/common/saveToImgByStr'
          }
        }
    },
    props: {

    },

    methods:{
      edit(record) {
        let { options } = this
        this.visible = true
        this.options = Object.assign({}, options, record)
      },

      cancelHandel() {
        this.options = {
          img: './avatar2.jpg',
          autoCrop: true,
          autoCropWidth: 200,
          autoCropHeight: 200,
          fixedBox: true
        }
        this.confirmLoading = false
        this.visible = false
      },
      okHandel() {
        const that = this
        that.confirmLoading = true
        // 获取截图的base64 数据
        this.$refs.cropper.getCropData((data) => {
          let file = this.base64ToFile(data, 'avatar.jpg')
          this.$emit('ok', {file: file, data:data})

        })
        setTimeout(() => {
          /* 延迟关闭表单 */
          that.cancelHandel()
        }, 1500);

      },
      //移动框的事件
      realTime(data) {
        this.previews = data
      },

      base64ToFile(urlData, fileName) {
        let arr = urlData.split(',');
        let mime = arr[0].match(/:(.*?);/)[1];
        let bytes = atob(arr[1]); // 解码base64
        let n = bytes.length
        let ia = new Uint8Array(n);
        while (n--) {
          ia[n] = bytes.charCodeAt(n);
        }
        return new File([ia], fileName, { type: mime });
      },
    },

    mounted(){

    },
}
</script>

<style scoped>
.avatar-upload-preview {
  position: absolute;
  top: 50%;
  transform: translate(50%, -50%);
  width: 300px;
  height: 300px;
  border-radius: 50%;
  box-shadow: 0 0 4px #ccc;
  overflow: hidden;
  img {
    width: 100%;
    height: 100%;
    }
}

</style>
