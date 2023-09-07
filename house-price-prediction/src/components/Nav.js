import React from 'react';
import { Link } from 'react-router-dom';

function Nav() {
    return (
        <nav>
            <ul>
                <li>
                    <Link to="/">首頁</Link>
                </li>
                <li>
                    <Link to="/rvr">實價登錄</Link>
                </li>
                {/* 添加其他導航連結 */}
            </ul>
        </nav>
    );
}

export default Nav;
