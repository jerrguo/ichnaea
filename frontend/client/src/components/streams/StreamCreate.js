import React from 'react';
import { reduxForm, Field } from 'redux-form'
import { Form, Button } from 'semantic-ui-react';
import { connect } from 'react-redux'
import { createStream } from './../../actions';
import StreamForm from './StreamForm';

class StreamCreate extends React.Component {

    render() {

        return (
            <div>
                <h3>Create a Stream</h3>
                <StreamForm onSubmit={this.props.createStream}></StreamForm>
            </div>)
    }
}


export default connect(null, { createStream })(StreamCreate);