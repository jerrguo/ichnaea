import React from 'react';
import { reduxForm, Field } from 'redux-form'
import { Form, Button } from 'semantic-ui-react';
import { connect } from 'react-redux'
import { editStream, fetchStream } from './../../actions';
import StreamForm from './StreamForm';

class StreamEdit extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.props.fetchStream(this.props.match.params.id)

    }

    onSubmit = (formValues) => {
        this.props.editStream(this.props.match.params.id, formValues)
    }


    render() {
        if (!this.props.stream) {
            return <div>Loading...</div>
        }
        return (
            <div>
                <h3>Edit Stream</h3>
                <StreamForm onSubmit={this.onSubmit} initialValues={{ title: this.props.stream.title, description: this.props.stream.description }}></StreamForm>
            </div>)
    }
}


const mapStateToProps = (state, ownProps) => {
    return {
        stream: state.streams[ownProps.match.params.id]
    }
}
export default connect(mapStateToProps, { editStream, fetchStream })(StreamEdit);