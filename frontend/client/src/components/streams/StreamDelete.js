import React from 'react';
import Modal from '../Modal';
import { Button } from 'semantic-ui-react';
import history from '../../history';
import { connect } from 'react-redux'
import { fetchStream, deleteStream } from './../../actions';
import { Link } from 'react-router-dom';

class StreamDelete extends React.Component {

    componentDidMount() {
        this.props.fetchStream(this.props.match.params.id)
    }


    renderActions() {
        const { id } = this.props.match.params;

        return (
            <React.Fragment>
                <Button negative onClick={() => this.props.deleteStream(id)}>Delete</Button>
                <Link to="/"><Button>Cancel</Button></Link>
            </React.Fragment>
        )
    }
    renderContent() {
        if (!this.props.stream) {
            return 'Are you sure you want to delete this stream?';
        }
        return `Are you sure you want to delete the stream with title: ${this.props.stream.title}`
    }
    render() {

        return (<div>
            <Modal title='Delete Stream' content={this.renderContent()}
                actions={this.renderActions()}
                onDismiss={() => history.push('/')} />
        </div >)
    }
}


const mapStateToProps = (state, ownProps) => {
    return {
        stream: state.streams[ownProps.match.params.id],
    }
}

export default connect(mapStateToProps, { fetchStream, deleteStream })(StreamDelete);