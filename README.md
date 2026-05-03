# procaptcha-pow

Proof-of-concept for the captcha provided by https://prosopo.io/.

All this project does is:
 - visit twickets.live 
 - grabs the page data and parses it to binary
 - generates a sr25519 polka address
 - requests the captcha for "pow" challenge tyoe
 - runs the pow challenge and submits it
 - generates a working token

Using https://twickets.live because it happened to contain this captcha challenge, no other reason.
