import Vue from "vue";

let vm = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',

        error_username: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,

        error_username_message: '1',
        error_mobile_message: "2"

    },
    methods: {
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
                    .get(url,{
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
                    .get(url,{
                        responseType: 'json'
                    })
                    .then(response => {
                        console.log(response.data)
                        if (response.data.count != 0){
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

            if (this.error_username || this.error_mobile || this.error_password || this.error_password2 || this.error_allow) {
                //window禁止提交表单
                console.log('前面有错误 error')
                return false
            }

        },
    }
});