/**
 * @param {String} fullAppId
 * @return {RegisterAppInterface}
 */
setFullAppId(fullAppId) {
    this.validateType(String, fullAppId);

    if (fullAppID != null) {
        fullAppID = fullAppID.toLowerCase();
        setParameters(RegisterAppInterface.KEY_FULL_APP_ID, fullAppID);
        let appID;
        if (fullAppID.length() <= RegisterAppInterface.APP_ID_MAX_LENGTH) {
            appID = fullAppID;
        } else {
            appID = fullAppID.replace("-", "").substring(0, RegisterAppInterface.APP_ID_MAX_LENGTH);
        }
        this._setAppId(appID);
    } else {
        setParameters(RegisterAppInterface.KEY_FULL_APP_ID, null);
    }

    return this;
}

/**
 * @return {String} the app id
 */
getFullAppId() {
    return this.getParameter(RegisterAppInterface.KEY_FULL_APP_ID);
}