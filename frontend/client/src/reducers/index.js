import { combineReducers } from 'redux';
import authReducer from './authReducer';
import { reducer } from 'redux-form';
import streamsReducer from './streamsReducer';

export default combineReducers({
    auth: authReducer,
    form: reducer,
    streams: streamsReducer
})