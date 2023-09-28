$(document).ready(function() {
    const vm = new Vue({
    delimiters: ['((', '))'],
    el: '#root',
    data: {
        current: 'none',
        add_appliance_window:'none',
        clock: '',
        progress: {},
        progress_face:{},
        user_img:'(( User_img ))',
        progress_text: '',
        canvas:null,
        canvas1:null,
        socket:null
    },
    methods: {
        change_window(need) {
            let progress_div = $('#progress')
            switch (need) {
                case 'login':
                    this.progress = {'width': '0%'}
                    this.progress_text = ''
                    break;
                case 'register1':
                    this.progress = {'width': '25%'}
                    this.progress_text = '设置邮箱，昵称'
                    break;
                case 'register2':
                    this.progress = {'width': '50%'}
                    this.progress_text = '获取验证码'
                    break;
                case 'register3':
                    this.progress = {'width': '75%'}
                    this.progress_text = '设置密码'
                    break;
                case 'register4':
                    this.progress = {'width':' 100%'}
                    this.progress_text = '面部录入'
                    break;
                case 'forget_password1':
                    this.progress = {'width': '33.3%'}
                    this.progress_text = '输入邮箱'
                    break;
                case 'forget_password2':
                    this.progress = {'width': '66.6%'}
                    this.progress_text = '面部识别找回'
                    break;
                case 'forget_password2_5':
                    this.progress = {'width': '66.6%'}
                    this.progress_text = '验证码找回'
                    break;
                case 'forget_password3':
                    this.progress = {'width': '100%'}
                    this.progress_text = '设置新密码'
                    break;
                default:
                    break
            }
            vm.current = need
        },
        close_window() {
            vm.close_camera(1)
            vm.close_camera(0)
            vm.current = 'none'
        },
        change_some_css(target, judgement) {
            let color = ''
            if (judgement === true) {
                color = 'green'
            }
            if (judgement === false) {
                color = 'red'
            }
            if (judgement === undefined) {
                color = 'gray'
            }
            target.css({
                'border': `2px solid ${color}`
            })
            target.next().css({
                'color': `${color}`,
            })
        },
        check_input_error(sentence){
            let illegal=new RegExp("(.+)\\sand\\s(.+)|(.+)\\sor(.+)\\s$")
            return illegal.test(sentence);
        },
        check_form_all_right(category) {
            if (category === 1) {
                let Register_Username = $(`#Register_Username`)
                if (Register_Username.val()) {
                    if (Register_Username.val().length < 4) {
                        this.change_some_css(Register_Username, false)
                    } else {
                        this.change_some_css(Register_Username, true)
                    }
                } else {
                    this.change_some_css(Register_Username, undefined)
                }
            }
            if (category === 2) {
                var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
                let Register_Email = $(`#Register_Email`)
                if (Register_Email.val()) {
                    if (reg.test(Register_Email.val())) {
                        this.change_some_css(Register_Email, true)
                    } else {
                        this.change_some_css(Register_Email, false)
                    }
                } else {
                    this.change_some_css(Register_Email)
                }
            }
            if (category === 3) {
                let agree1 = $(`#agree1`).is(':checked')
                let agree2 = $(`#agree2`).is(':checked')
                if (agree1 === true && agree2 === true) {
                    $("#register1_next").removeAttr("disabled");
                }
                if (agree1 === false || agree2 === false) {
                    $("#register1_next").attr("disabled", "disabled");
                }
            }
            if (category === 4) {
                let Register_Password = $(`#Register_password`)
                let tip1=$(`#Register_password_tip1`)
                if (Register_Password.val()) {
                    if (Register_Password.val().length > 5) {
                        this.change_some_css(Register_Password, true)
                        tip1.css('color','rgb(0, 128, 0)')
                        tip1.text('正确')
                    } else {
                        this.change_some_css(Register_Password, false)
                        tip1.css('color','rgb(255, 0, 0)')
                        tip1.text('密码至少6位')
                    }
                } else {
                    this.change_some_css(Register_Password, undefined)
                    tip1.text(' ')
                }
            }
            if (category === 5){
                let tip2=$(`#Register_password_tip2`)
                let Register_Password = $(`#Register_password`)
                let Register_Password_Confirm=$(`#Register_password_confirm`)
                if (Register_Password_Confirm.val()){
                    if (Register_Password.val()===Register_Password_Confirm.val()){
                        this.change_some_css(Register_Password_Confirm, true)
                        tip2.css('color','rgb(0, 128, 0)')
                        tip2.text('正确')
                    }
                    else {
                        this.change_some_css(Register_Password_Confirm, false)
                        tip2.css('color','rgb(255, 0, 0)')
                        tip2.text('两次密码匹配不一致')
                    }
                }else {
                    this.change_some_css(Register_Password_Confirm, undefined)
                    tip2.text(' ')
                }
            }
            if (category === 6) {
                let Register_Password = $(`#Forget_password`)
                let tip1=$(`#Forget_password_tip1`)
                if (Register_Password.val()) {
                    if (Register_Password.val().length > 5) {
                        this.change_some_css(Register_Password, true)
                        tip1.css('color','rgb(0, 128, 0)')
                        tip1.text('正确')
                    } else {
                        this.change_some_css(Register_Password, false)
                        tip1.css('color','rgb(255, 0, 0)')
                        tip1.text('密码至少6位')
                    }
                } else {
                    this.change_some_css(Register_Password, undefined)
                    tip1.text(' ')
                }
            }
            if (category === 7){
                let tip2=$(`#Forget_password_tip2`)
                let Forget_Password = $(`#Forget_password`)
                let Forget_Password_Confirm=$(`#Forget_password_confirm`)
                if (Forget_Password_Confirm.val()){
                    if (Forget_Password.val()===Forget_Password_Confirm.val()){
                        this.change_some_css(Forget_Password_Confirm, true)
                        tip2.css('color','rgb(0, 128, 0)')
                        tip2.text('正确')
                    }
                    else {
                        this.change_some_css(Forget_Password_Confirm, false)
                        tip2.css('color','rgb(255, 0, 0)')
                        tip2.text('两次密码匹配不一致')
                    }
                }else {
                    this.change_some_css(Register_Password_Confirm, undefined)
                    tip2.text(' ')
                }
            }
        },
        alert_window(text, id) {
            let alert_w = $(`#${id}`);
            alert_w.text(text);
            alert_w.css('display', 'block');
            setTimeout( () => {
                alert_w.fadeOut('slow');
            }, 3000);
        },
        register1_next() {
            let Register_Username = $(`#Register_Username`)
            let Register_Email = $(`#Register_Email`)
            let nothing_in_input = '1.6px solid rgb(128, 128, 128)'
            let right_input = '1.6px solid rgb(0, 128, 0)'
            let error_input = '1.6px solid rgb(255, 0, 0)'
            console.log(Register_Username.css('border'))
            if (Register_Username.css('border') !== nothing_in_input) {
                if (Register_Username.css('border') === error_input) {
                    this.alert_window('用户名Username过短，至少4位', 'Error_window')
                }
                if (Register_Username.css('border') === right_input) {
                    if (Register_Email.css('border') !== nothing_in_input) {
                        if (Register_Email.css('border') === error_input) {
                            this.alert_window('邮箱Email不合法', 'Error_window')
                        } else {
                            $(`#loading_success`).css('display', 'block')
                            let data_dict = {
                                'Register_Username': Register_Username.val(),
                                'Register_Email': Register_Email.val()
                            }
                            var temp_num=0
                            if (Register_Email.css('border') === right_input) {
                                $.ajax({
                                    type: 'POST',
                                    url: '/user/register1_send_captcha',
                                    data: data_dict,
                                    success: function (result) {
                                        console.log(result)
                                        if (result==='OK'){
                                            $(`#loading_success`).css('display', 'none')
                                            vm.alert_window('验证码已经成功发送到您的邮箱','success')
                                            vm.change_window('register2')
                                        }
                                        else if (result==='Wrong'){
                                            $(`#loading_success`).css('display', 'none')
                                            vm.alert_window('授权码过期，请联系管理员修改', 'Error_window')
                                        }else if(result==='repeat1') {
                                            $(`#loading_success`).css('display', 'none')
                                            vm.alert_window('用户名重复','Error_window')
                                        }
                                        else {
                                            $(`#loading_success`).css('display', 'none')
                                            vm.alert_window('该邮箱已经被注册','Error_window')
                                        }
                                    },
                                    error: function () {
                                        $(`#loading_success`).css('display', 'none')
                                        vm.alert_window('发生未知错误', 'Error_window')
                                    }
                                })
                            }
                        }
                    } else {
                        this.alert_window('请输入您的邮箱Email', 'Error_window')
                    }
                }
            } else {
                this.alert_window('请输入您的用户名Username', 'Error_window')
            }
        },
        focusNextInput(thisinput) {
            if(thisinput.keyCode!==8 && thisinput.target.value){
                thisinput.currentTarget.nextElementSibling.focus()
            }
        },
        focusPrevInput(thisinput){
            thisinput.currentTarget.previousElementSibling.focus()
        },
        register2_next(){
            let inputs=$(`.get_captcha input`)
            let temp_captcha=''
            for(let i=0;i<inputs.length;i++){
                temp_captcha=temp_captcha+inputs.eq(i).val()
            }
            $.ajax({
                type: 'POST',
                url: '/user/register2_get_captcha',
                data: {'captcha':temp_captcha},
                success: function (result) {
                    if(result==='OK'){
                        vm.alert_window('给你小子蒙对了','Success_window')
                        vm.change_window('register3')
                    }
                    else if(result==='NO'){
                        vm.alert_window('你小子没输入对','Error_window')
                    }
                    else{
                        vm.alert_window('验证码超时或已被黑客截取了你的验证码抢先注册了','Error_window')
                    }
                },
                error: function () {
                    vm.alert_window(`被黑客入侵了我真无语,拿了什么跟我说一下`,`Error_window`)
                }
            })
        },
        register3_next(){
            let Register_Password = $(`#Register_password`)
            let Register_Password_Confirm=$(`#Register_password_confirm`)
            let nothing_in_input = '1.6px solid rgb(128, 128, 128)'
            let right_input = '1.6px solid rgb(0, 128, 0)'
            let error_input = '1.6px solid rgb(255, 0, 0)'
            if (Register_Password.css('border')===right_input){
                if (Register_Password_Confirm.css('border')===right_input){
                    $.ajax({
                        type:'POST',
                        url:'/user/register3',
                        data:{'password':Register_Password.val()},
                        success:function (result){
                            if (result==='OK'){
                                vm.alert_window('注册成功，及将为你跳转到人脸识别。','Success_window')
                                vm.change_window('register4')
                            }
                            else {
                                alert(result)
                            }
                        },
                        error:function (){
                            vm.alert_window('含有非法字符,或注册时间过长。','Error_window')
                        }
                    })
                }else{
                    vm.alert_window('两次输入的密码不一致','Error_window')
                }
            }else if (Register_Password.css('border')===error_input){
                vm.alert_window(`密码过短，容易被破解，最好大于6位`,'Error_window')
            }else{
                vm.alert_window(`密码不能为空，最好大于6位`,'Error_window')
            }
        },
        change_user_img(){
        },
        to_login(){
            let Password=$(`#Password`).val()
            let Email=$(`#Email`).val()
            if (Password){
                if (Email){
                    $.ajax({
                        type:'POST',
                        url:`/user/login`,
                        data:{'Email':Email,'Password':Password},
                        success:function (result){
                            if (result==='OK'){
                                vm.alert_window('登陆成功','Success_window')
                                window.location='/'
                            }
                            else if (result==='ATTACK'){
                                vm.alert_window('坏了，你小子号被别人登录中','Error_window')
                            }
                            else if(result==='Wrong'){
                                alert('我真就草泥马了，这点B水平还SQL注入拟注入尼玛注入')
                            }
                            else if(result==='Error'){
                                vm.alert_window(`密码错误`,'Error_window')
                            }else if(result==='None'){
                                vm.alert_window('邮箱不存在，请先注册','Error_window')
                            }
                        }
                    })
                }else {
                    vm.alert_window('请输入密码','Error_window')
                }
            }else {
                vm.alert_window('请输入请输入邮箱','Error_window')
            }
        },
        action(){
            const media = $(`#media`)	// video元
            const canvas= document.getElementById('photo')
            var v = document.querySelector('video')
            var ctx = canvas.getContext('2d')
            ctx.drawImage(v, 0, 0, 480, 320)
            var oGrayImg = canvas.toDataURL('image/jpeg')
            console.log(oGrayImg)
            var form = new FormData();
            form.append("file", oGrayImg);
            console.log(form)
            $.ajax({
                type: 'POST',
                url: '/user/register4_enter_face',
                data: form,
                processData: false,   // 不处理发送的数据
                contentType: false,   // 不设置Content-Type请求头
                success(result) {
                   if(result==='ERROR'){
                       vm.alert_window('TMD出错了','Error_window')
                   }
                   else if(result==='Too much'){
                       vm.alert_window('人脸过多','Error_window')
                   }
                   else if(result==='None'){
                       vm.alert_window('未检测到人脸，请重试','Error_window')
                   }
                   else {
                       vm.alert_window('金色传说，注册完成','Success_window')
                       vm.change_window('login')
                       vm.close_camera(0)
                   }
                },
            })
        },
        forget_password(flag){
            console.log(flag)
            let Email_onforget=$(`#Email_onforget`).val()
            $.ajax({
                type:'POST',
                url:'/user/forget_password1',
                data:{'Email_onforget':Email_onforget},
                success(result){
                    if (result==='Warning'){
                        vm.alert_window('还SQL注入你是不是有毛病','Error_window')
                    }
                    else if(result==='NONE'){
                        vm.alert_window('该邮箱不存在请先注册','Error_window')
                    }
                    else{
                        vm.alert_window(result,'Success_window')
                        if(flag===1)
                        {
                            vm.change_window('forget_password2')
                            vm.open_camera(1)
                        }
                        if(flag===2){
                            vm.change_window('forget_password2_5')
                        }
                    }
                }
            })
            },
        open_camera(temp){
            if(temp===0){
                vm.media = document.getElementById('media')	// video元素
                vm.canvas = document.getElementById('photo')
            }
            else {
                vm.media = document.getElementById('media1')	// video1元素
                vm.canvas = document.getElementById('photo1')//
            }
            navigator.mediaDevices.getUserMedia({video: {width: 480, height: 320}, audio: true}).then(stream => {
            // 将视频流设置为video元素的源
            vm.media.srcObject = stream
            // 低版本浏览器
            // media.src = window.URL.createObjectURL(stream)
            vm.media.play()
            if (temp===1) {
                vm.socket = io();
                let intervalId = setInterval(
                    () => {
                    vm.canvas.getContext('2d').drawImage(vm.media, 0, 0);
                    const data = vm.canvas.toDataURL('image/jpeg');
                    vm.socket.emit('video_frame1', data, function (result) {
                        if (result === 'success') {
                            clearInterval(intervalId);
                            vm.alert_window('识别成功', 'Success_window')
                            vm.socket.disconnect()
                            vm.close_camera(1)
                            vm.change_window('forget_password3')
                        } else {
                            if (result<-50){
                                vm.close_camera(1)
                                vm.change_window('login')
                                vm.alert_window('识别失败','Error_window')
                            }
                            vm.progress_face={'width': result*2+'%'}
                        }
                    });  // 发送 'video_frame' 事件至服务器
                }, 100);  // 每100毫秒发送一次帧
            }
            }).catch(err => {
                vm.alert_window('摄像头被占用啦，你是不是跟你女朋友打电话呢啊？','Error_window')
            });
        },
        close_camera(temp){
            if(temp===0){
                vm.media = document.getElementById('media')	// video元素
            }
            else {
                vm.media = document.getElementById('media1')	// video元素
            }
            if (vm.media && vm.media.srcObject) {
                let tracks = vm.media.srcObject.getTracks();
                tracks.forEach(track => track.stop());
                vm.media.srcObject = null;
                vm.socket.disconnect()
            }
        },
        forget3_next(){
            const password=$(`#Forget_password`).val()
            const password_conform=$(`#Forget_password_confirm`).val()
            console.log(password)
            console.log(password_conform)
            if (password===password_conform){
                var data_dict={'password':password}
                $.ajax({
                    type:'POST',
                    url:'/user/forget_password3',
                    data:data_dict,
                    success(result){
                        if (result==='OK'){
                            vm.alert_window('成功，你他娘的太傻逼了，自己密码都会忘','Success_window')
                            vm.change_window('login')
                        }
                        else if (result==='Warning'){
                            alert('我真就草泥马了，这点B水平还SQL注入拟注入尼玛注入')
                        }
                        else{
                            vm.alert_window(result,'Error_window')
                        }
                    }
                })
            }
            else {
                vm.alert_window('两次密码输入不一致','Error_window')
            }
        }
    },
    watch: {
        current: {
            handler(need, old_value) {
                if (need !== 'none') {
                    if (old_value !== 'none') {
                        $(`#${old_value}`).css('display', 'none')
                    } else {
                        $('#tanchuang').css('display', 'block')
                    }
                } else {
                    $(`#${old_value}`).css('display', 'none')
                    $('#tanchuang').css('display', 'none')
                    return
                }
                $(`#${need}`).css('display', 'flex')
            }
        },
    },
    mounted(){
        var canvas=document.getElementById('photo')
        var context = canvas.getContext('2d')
        var canvas1=document.getElementById('photo1')
        var context1 = canvas1.getContext('2d')
    }
})
})