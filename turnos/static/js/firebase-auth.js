// Firebase authentification

// Firebase initApp
function initApp() {
    // Listening for auth state changes
    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            // User is signed in
            var displayName = user.displayName;
            var email = user.email;
            var emailVerified = user.emailVerified;
            var photoURL = user.photoURL;
            var isAnonymous = user.isAnonymous;
            var uid = user.uid;
            var providerData = user.providerData;
            // Logged with
            providerData.forEach(data => {
                if (data['providerId'] == 'google.com') {
                    document.getElementById('firebase-sign-in-google-status').textContent = 'Abierta';
                    document.getElementById('firebase-sign-in-google').textContent = 'Cerrar cuenta de Google';
                }
            });
            //document.getElementById('firebase-account-details').textContent = JSON.stringify(user, null, '  ');
            document.getElementById('firebase-account-details').textContent = JSON.stringify(providerData, null, '  ');
            var welcomeUser = displayName ? displayName : email;
            document.getElementById('user').textContent = welcomeUser;
            user.getIdToken().then(function (idToken) {
                document.getElementById('email').setAttribute('value', user.email);
                document.getElementById('token').setAttribute('value', idToken);
                document.getElementById('firebase-logged-out').style.display = 'none';
                document.getElementById('firebase-logged-in').style.display = 'inline';
                document.getElementById('access-form-firebase').style.display = 'inline';
            });
        } else {
            // User is signed out
            document.getElementById('firebase-sign-in-google').textContent = 'Google';
            document.getElementById('firebase-sign-in-google-status').textContent = 'Cerrada';
            document.getElementById('firebase-sign-in-github').textContent = 'GitHub';
            document.getElementById('firebase-sign-in-github-status').textContent = 'Cerrada';
            document.getElementById('firebase-sign-in-microsoft').textContent = 'Microsoft';
            document.getElementById('firebase-sign-in-microsoft-status').textContent = 'Cerrada';
            document.getElementById('firebase-account-details').textContent = 'null';
            //document.getElementById('quickstart-oauthtoken').textContent = 'null';
            document.getElementById('firebase-logged-out').style.display = 'inline';
            document.getElementById('firebase-logged-in').style.display = 'none';
            document.getElementById('access-form-firebase').style.display = 'none';
        }
        document.getElementById('firebase-sign-in-google').disabled = false;
        document.getElementById('firebase-sign-in-github').disabled = false;
        document.getElementById('firebase-sign-in-microsoft').disabled = false;
    });
    // Add listeners in buttons
    document.getElementById('firebase-sign-in-google').addEventListener('click', googleToggleSignIn, false);
    document.getElementById('firebase-sign-in-github').addEventListener('click', githubToggleSignIn, false);
    document.getElementById('firebase-sign-in-microsoft').addEventListener('click', microsoftToggleSignIn, false);
}
