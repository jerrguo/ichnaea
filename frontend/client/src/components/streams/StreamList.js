import React from 'react';
import { Item, Button, Icon, List } from 'semantic-ui-react';
import { connect } from 'react-redux'
import { fetchStreams } from './../../actions';
import { Link } from 'react-router-dom';

class StreamList extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.props.fetchStreams();
    }

    renderAdmin = (stream) => {
        if (stream.userId === this.props.userId) {
            return (
                <List.Content floated='right'>
                    <Link to={`/streams/edit/${stream.id}`}><Button primary>Edit</Button></Link>
                    <Link to={`/streams/delete/${stream.id}`}><Button negative>Delete</Button></Link>
                </List.Content>
            )
        }
        return null;
    }
    renderList() {
        return this.props.streams.map(stream => {
            return (<Item key={stream.id}>
                {this.renderAdmin(stream)}
                <Icon name="camera" size="large" ></Icon>
                <List.Content>
                    <Link to={`/streams/${stream.id}`} className="header">{stream.title}</Link>
                    <Item.Description>
                        {stream.description}
                    </Item.Description>
                </List.Content>
            </Item>)
        })
    }

    renderCreate() {
        if (this.props.isSignedIn) {
            return <div style={{ textAlign: 'right' }}><Link to="/streams/new"><Button primary>Create Stream</Button></Link></div>
        }
    }
    render() {

        return (<div>
            <h2>Streams</h2>
            <List celled>{this.renderList()}</List>
            {this.renderCreate()}
        </div>)
    }
}

const mapStateToProps = (state) => {
    return {
        streams: Object.values(state.streams),
        userId: state.auth.userId,
        isSignedIn: state.auth.isSignedIn
    }
}

export default connect(mapStateToProps, { fetchStreams })(StreamList);