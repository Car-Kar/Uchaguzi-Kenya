import React from 'react';

class Footer extends React.Component {
    render() {
        return (
            <footer>
                <div id = "footer">
                    <div id = "media" className = "footer">
                        <ul>
                            <li><a href = "#"><i className = "fab fa-facebook-f"></i></a></li>
                            <li><a href = "#"><i className = "fab fa-facebook-messenger"></i></a></li>
                            <li><a href = "#"><i className = "fab fa-twitter"></i></a></li>
                        </ul>

                    </div>
                </div>
            </footer>
        )
    }
}

export default Footer;