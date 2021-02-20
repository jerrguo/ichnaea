import React from "react";
import { Button, Icon } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { signIn, signOut } from './../actions';


class GoogleAuth extends React.Component {
    componentDidMount() {
        console.log(process.env.REACT_APP_OAUTH_CLIENT_ID)
        window.gapi.load("auth2", () => {
            window.gapi.auth2
                .init({
                    clientId: process.env.REACT_APP_OAUTH_CLIENT_ID,
                    scope: "email"
                })
                .then(() => {
                    this.auth = window.gapi.auth2.getAuthInstance();
                    this.onAuthChange(this.auth.isSignedIn.get());
                    this.auth.isSignedIn.listen(this.onAuthChange)
                });
        });
    }

    onAuthChange = (isSignedIn) => {
        if (isSignedIn) {
            this.props.signIn(this.auth.currentUser.get().getId());
        }
        else {
            this.props.signOut();
        }
    }

    onSignInClick = () => {
        this.auth.signIn()
    }
    onSignOutClick = () => {
        this.auth.signOut()
    }

    render() {
        if (this.props.isSignedIn == null) {
            return null;
        }
        else if (this.props.isSignedIn) {
            return <Button secondary onClick={this.onSignOutClick}><Icon name='google' />Sign Out</Button>
        }
        else {
            return <Button primary onClick={this.onSignInClick}><Icon name='google' />Sign In</Button>
        }
    }
}
const mapStateToProps = (state) => {
    return { isSignedIn: state.auth.isSignedIn }
}

export default connect(mapStateToProps, { signIn, signOut })(GoogleAuth);
