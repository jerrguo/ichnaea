import ACTIONS from './../actions/constants';
import _ from 'lodash';


const INITIAL_STATE = {}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case ACTIONS.FETCH_STREAMS: ;
            return { ...state, ..._.mapKeys(action.payload, 'id') }
        case ACTIONS.EDIT_STREAM:
            return { ...state, [action.payload.id]: action.payload };
        case ACTIONS.FETCH_STREAM:
            return { ...state, [action.payload.id]: action.payload };
        case ACTIONS.CREATE_STREAM:
            return { ...state, [action.payload.id]: action.payload };
        case ACTIONS.DELETE_STREAM:
            return _.omit(state, action.payload);
        default:
            return state;
    }
}