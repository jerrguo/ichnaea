import React from "react";
import ReactDOM from "react-dom";
import { Button, Modal, Header } from 'semantic-ui-react';

const Dialog = (props) => {
    return ReactDOM.createPortal(
        (<div onClick={props.onDismiss}>
            <Modal open={true} onClick={(e) => e.stopPropagation()}>
                <Modal.Content>
                    <Modal.Description>
                        <Header>{props.title}</Header>
                        <p>{props.content}</p>
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    {props.actions}
                </Modal.Actions>
            </Modal>
        </div>),
        document.querySelector('#modal')
    )
}

export default Dialog;
