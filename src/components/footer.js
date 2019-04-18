import React from 'react';

class Footer extends React.Component {
    render() {
        return (
            <footer>
                <div id = "footer" className = "container fluid">
                    <div id = "media" className = "footer">
                        <ul className = "navbar-nav mx-auto text-center">
                            <li><a href = "#"><i className = "fab fa-facebook-f"></i></a></li>
                            <li><a href = "#"><i className = "fab fa-facebook-messenger"></i></a></li>
                            <li><a href = "#"><i className = "fab fa-twitter"></i></a></li>
                            <li><a href = "https://github.com/wambu-i/Jumuiya"><i className = "fab fa-github"></i></a></li>
                        </ul>
                    </div>
                    <div id = "credits" className = "mx-auto text-center">
                        <span>© 2019 Jumuiya</span>
                    </div>
                </div>
            </footer>
        )
    }
}

export default Footer;