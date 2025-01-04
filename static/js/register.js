let vm = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        uuid: '',
        image_code_url: '',
        image_code: '',
        msg_code: '',
        msg_code_tip: '获取短信验证码',
        can_send_msg_flag: true,

        error_username: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_msg_code: false,

        error_username_message: '1',
        error_mobile_message: "2",
        error_image_code_message: "",
        error_msg_code_message: "",

    },
    mounted() {
        // 生成图形验证码
        this.generate_image_code()
    },
    methods: {
        // 发送短信验证码
        send_msg() {
            if (this.can_send_msg_flag === false) {
                return
            }
            this.can_send_msg_flag = false
            //     判断图片验证码
            this.check_image_code()
            this.check_mobile()
            // axios发送请求
            let url = "/sms_codes/" + this.mobile + "/?image_code=" + this.image_code + "&uuid=" + this.uuid
            axios.get(url, {
                responseType: 'json'
            })
                // 成功
                .then((response) => {
                    if (response.data.code === "0") {
                        // 成功
                        this.error_msg_code = false
                        // 倒计时
                        let count = 60
                        let timer = setInterval(() => {
                            if (count === 1) {
                                clearInterval(timer)
                                this.msg_code_tip = '获取短信验证码'
                                this.error_msg_code = false
                                this.can_send_msg_flag = true
                            }
                            count -= 1
                            this.msg_code_tip = count + '秒'

                        }, 1000, 60)

                    } else if (response.data.code === "4001") {
                        // 图形验证码错误
                        this.error_msg_code = true
                        this.error_image_code_message = response.data.errmsg
                    } else if (response.data.code === "4002") {
                        // 短信发送太过频繁
                        this.error_msg_code = true
                        this.error_msg_code_message = response.data.errmsg
                    } else {
                        this.can_send_msg_flag = true
                    }
                })
                // 失败了
                .catch((error) => {
                    console.log(error)
                })

        },
        // 确认短信验证码
        check_msg_code() {
            if (!this.msg_code) {
                this.error_msg_code_message = '请填写短信验证码'
                this.error_msg_code = true
            } else {
                this.error_msg_code = false
            }
        },
        // 确认图形码
        check_image_code() {
            if (!this.image_code) {
                this.error_image_code_message = "请填写图片验证码"
                this.error_image_code = true
            } else {
                this.error_image_code = false
            }
        },
//         生成图形验证码
        generate_image_code() {
            this.uuid = generateUUID()
            this.image_code_url = '/image_codes/' + this.uuid + '/'
        },
// 校验用户名
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false
            } else {
                this.error_username_message = "请输入5-20个字符"
                this.error_username = true
            }
            // 用户名称是否重复
            if (!this.error_username) {
                let url = '/usernames/' + this.username + '/count/'
                axios
                    .get(url, {
                        responseType: 'json',
                    })
                    .then(response => {
                        console.log(response.data)
                        if (response.data.count === 1) {
                            this.error_username = true
                            this.error_username_message = "用户名已存在"
                        }
                    })
                    .catch(error => {
                        console.log(error.response)
                    })
            }
        },
        // 校验密码
        check_password() {
            let re = /^[A-Za-z0-9_-]{8,20}$/

            this.error_password = !re.test(this.password);
        },
        // 校验确认密码
        check_password2() {
            this.error_password2 = this.password !== this.password2
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            this.error_mobile = !re.test(this.mobile);

            if (this.error_mobile) {
                this.error_mobile_message = "手机号格式不正确"
            }
            // 验证手机号是否重复
            if (!this.error_mobile) {
                let url = '/mobiles/' + this.mobile + '/count/'
                axios
                    .get(url, {
                        responseType: 'json'
                    })
                    .then(response => {
                        console.log(response.data)
                        if (response.data.count !== 0) {
                            this.error_mobile = true
                            this.error_mobile_message = '手机号重复'
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        // 校验是否勾选协议
        check_allow() {
            this.error_allow = !this.allow;
        },
        // 监听表单提交事件
        on_submit(event) {
            // event.preventDefault();
            this.check_allow()
            this.check_username()
            this.check_mobile()
            this.check_password()
            this.check_password2()
            this.check_image_code()
            this.check_msg_code()

            if (this.error_username || this.error_mobile || this.error_password || this.error_password2 || this.error_allow || this.error_image_code || this.error_msg_code) {
                //window禁止提交表单
                console.log('前面有错误 error')
                return false
            }

        },
    }
});