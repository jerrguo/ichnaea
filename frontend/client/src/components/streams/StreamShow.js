import React from 'react';
import { reduxForm, Field } from 'redux-form'
import { Form, Button } from 'semantic-ui-react';
import { connect } from 'react-redux'
import { fetchStream } from './../../actions';
import StreamForm from './StreamForm';
import flv from 'flv.js';
class StreamShow extends React.Component {

    constructor(props) {
        super(props);
        this.videoRef = React.createRef();
    }
    componentDidMount() {
        const { id } = this.props.match.params;
        this.props.fetchStream(id);
        this.buildPlayer();
    }

    componentDidUpdate() {
        this.buildPlayer();
    }

    componentWillUnmount() {
        this.player.destroy();
    }

    buildPlayer() {
        if (this.player || !this.props.stream) {
            return;
        }
        const { id } = this.props.match.params;
        if (flv.isSupported()) {
            this.player = flv.createPlayer({
                type: 'flv',
                url: `http://localhost:8000/live/${id}.flv`
            });
            this.player.attachMediaElement(this.videoRef.current);
            this.player.load();
        }
        var link = document.createElement("a"); //create 'a' element
        link.setAttribute("href", `http://localhost:8000/live/${id}.flv`); //replace "file" with link to file you want to download
        link.setAttribute("download", `http://localhost:8000/live/${id}.flv`);// replace "file" here too
        link.click(); //virtually click <a> element to initiate download


    }
    render() {
        if (!this.props.stream) {
            return <div>Loading...</div>
        }
        return (
            <div>
                <video ref={this.videoRef} style={{ width: '100%' }} controls></video>
                <h1>{this.props.stream.title}</h1>
                <h5>{this.props.stream.description}</h5>

            </div>)
    }
}
const mapStateToProps = (state, ownProps) => {
    return {
        stream: state.streams[ownProps.match.params.id]
    }
}

export default connect(mapStateToProps, { fetchStream })(StreamShow);