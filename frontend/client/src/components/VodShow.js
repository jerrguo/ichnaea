import React from 'react';
import { reduxForm, Field } from 'redux-form'
import { Form, Button } from 'semantic-ui-react';
import { connect } from 'react-redux'
import { fetchVod } from './../actions';
import flv from 'flv.js';
import videojs from 'video.js'
class VodShow extends React.Component {

    constructor(props) {
        super(props);
        this.videoRef = React.createRef();
    }
    componentDidMount() {
        const { id } = this.props.match.params;
        this.props.fetchVod(id);
        
        this.buildPlayer();
    }

    componentWillUnmount() {
        if (this.player) {
            this.player.dispose()
          }
    }

    buildPlayer() {
        if (this.player || !this.props.vod) {
            return;
        }
        this.player = videojs(this.videoNode, this.props, function onPlayerReady() {
            console.log('Video.js Ready', this)
          });

    }
    render() {
        const { id } = this.props.match.params;
        var source = "http://dm1hejhmfpfwk.cloudfront.net/" + id;
        return (<div>
            <h2>Vod</h2>
            <video id="example_video_1" class="video-js vjs-default-skin"
            controls preload="auto" width="1600" height="900">
            <source src={source} type='video/mp4' />
            </video>
        </div>)
        
    }
}
const mapStateToProps = (state, ownProps) => {
    return {
        vod: state.vods[ownProps.match.params.id]
    }
}

export default connect(mapStateToProps, { fetchVod })(VodShow);