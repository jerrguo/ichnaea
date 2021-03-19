import ACTIONS from './constants';
import streams from '../apis/streams';
import vods from '../apis/vods';
import history from './../history';

export const signIn = (userId) => {
    return {
        type: ACTIONS.SIGN_IN,
        payload: userId
    };
}

export const signOut = () => {
    return {
        type: ACTIONS.SIGN_OUT
    };
}

export const fetchVods = () => {
    return async (dispatch) => {
        const response = await vods.get('/vods');
        dispatch({
            type: ACTIONS.FETCH_VODS,
            payload: response.data
        })
    }
}

export const fetchVod = (id) => {
    return async (dispatch) => {
        const response = await streams.get(`/vods/${id}`);
        dispatch({
            type: ACTIONS.FETCH_VOD,
            payload: response.data
        })
    }
}

export const createStream = (formValues) => {
    return async (dispatch, getState) => {
        const { userId } = getState().auth;
        const response = await streams.post('/streams', { ...formValues, userId });
        dispatch({
            type: ACTIONS.CREATE_STREAM,
            payload: response.data
        })
        history.push('/')
    }
}

export const fetchStreams = () => {
    return async (dispatch) => {
        const response = await streams.get('/streams');
        dispatch({
            type: ACTIONS.FETCH_STREAMS,
            payload: response.data
        })
    }
}

export const fetchStream = (id) => {
    return async (dispatch) => {
        const response = await streams.get(`/streams/${id}`);
        dispatch({
            type: ACTIONS.FETCH_STREAM,
            payload: response.data
        })
    }
}
export const editStream = (id, formValues) => {
    return async (dispatch) => {
        const response = await streams.patch(`/streams/${id}`, formValues);
        dispatch({
            type: ACTIONS.EDIT_STREAM,
            payload: response.data
        })
        history.push('/')

    }
}

export const deleteStream = (id) => {
    return async (dispatch) => {
        await streams.delete(`/streams/${id}`);
        dispatch({
            type: ACTIONS.DELETE_STREAM,
            payload: id
        })
        history.push('/')
    }
}