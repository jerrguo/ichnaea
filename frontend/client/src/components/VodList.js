import React from "react";
import { Item, Button, Icon, List } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { fetchVods } from '../actions';
import { Link } from 'react-router-dom';

var array= [];

class VodList extends React.Component {
    componentDidMount() {
    }

    renderList() {
        const AWS = require('aws-sdk')
        const s3 = new AWS.S3()

        AWS.config.update({region: 'us-east-1'});
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'us-east-1:8ded4c54-a9fe-4a13-a1ae-2467840f86e8',
        });
        var bucketParams = {
            Bucket : 'cf-simple-s3-origin-cloudfrontfors3-778103269065',
        };
        
        
        s3.listObjects(bucketParams, function(err, data) {
            array.length = 0;
            if (err) {
              console.log("Error", err);
              return null;
            } else {
              console.log("Success", data.Contents[0].Key);
              data.Contents.forEach(e => array.push(e));
              return array.map(a => {
                return (<Item key={a.Key}>
                    <Icon name="camera" size="large" ></Icon>
                    <List.Content>
                        <Link to={`/vods/${a.Key}`} className="header">{a.Key}</Link>
                    </List.Content>
                </Item>)
            })  
            }
        });
    }

    render() {
        this.renderList();

        return (<div>
            <h2>Vods</h2>
            <List celled>{array.map(a => {
            return (<Item key={a.Key}>
                <List.Content>
                    <Link to={`/vods/${a.Key}`} className="header">{a.Key}</Link>
                </List.Content>
            </Item>)
        })}</List>
        </div>)
    }
}
const mapStateToProps = (state) => {
    return {
        userId: state.auth.userId,
        isSignedIn: state.auth.isSignedIn
    }
}
export default connect(mapStateToProps, { fetchVods })(VodList);
