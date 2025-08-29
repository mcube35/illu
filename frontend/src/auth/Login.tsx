import { useState } from "react";
import './Login.css';

const Login: React.FC = () => {
    const [userName, setUserName] = useState('')
    const [pwd, setPwd] = useState('')

    return (
        <div className="LoginFrame">
            <div className="LoginForm">
                <label>로그인 화면</label>
                <div>
                    <label>UserName</label>
                    <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)} />
                </div>
                <div>
                    <label>Password</label>
                    <input type="password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
                </div>
                    <button>로그인</button>
                <div>
                    <label>계정이 없으신가요? ㅋ</label>
                </div>
            </div>
        </div>
    )
}
export default Login;