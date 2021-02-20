import ACTIONS from './../actions/constants';



const INITIAL_STATE = {
    isSignedIn: null,
    userId: null
}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case ACTIONS.SIGN_IN:
            return { ...state, isSignedIn: true, userId: action.payload }
        case ACTIONS.SIGN_OUT:
            return { ...state, isSignedIn: false, userId: null }
        default:
            return state;
    }
}