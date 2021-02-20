import React from 'react';
import { reduxForm, Field } from 'redux-form'
import { Form, Button } from 'semantic-ui-react';

class StreamForm extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {

    }
    onSubmit = (formValues) => {
        this.props.onSubmit(formValues)
    }


    renderInput = ({
        input,
        label,
        type,
        meta
    }) => {
        let errMsg = meta.touched && (meta.error || meta.warning);
        return (
            <Form.Field>
                <label>{label}</label>
                <Form.Input {...input} type={type} onChange={input.onChange} value={input.value} error={errMsg || null} />
            </Form.Field >
        )
    }

    render() {

        return (<Form onSubmit={this.props.handleSubmit(this.onSubmit)}>

            <Field name="title" type="text" component={this.renderInput} label="Enter Title"></Field>
            <Field name="description" type="text" component={this.renderInput} label="Enter Description"></Field>
            <Button type='submit' primary disabled={this.props.submitting}>Submit</Button>
        </Form>)
    }
}

const validate = (formValues) => {
    const errors = {};
    if (!formValues.title) {
        errors.title = 'You must enter a title'
    }
    if (!formValues.description) {
        errors.description = 'You must enter a description'
    }
    return errors;
}

const formWrapepd = reduxForm({
    form: 'streamForm',
    validate: validate
})(StreamForm);


export default formWrapepd;