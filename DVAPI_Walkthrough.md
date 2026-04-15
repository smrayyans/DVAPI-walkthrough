# DVAPI Walkthrough

## API1:2023 — Broken Object Level Authorization

Navigate to profile page and intercept traffic in Burp. Spot the request loading the current user's note — `GET /api/getNote?username=rayyanshah04`.

![](images/api1-01-getnote-original-request.png)

Change the `username` parameter to another user (`test1`) while keeping the JWT unchanged.

![](images/api1-02-getnote-username-modified.png)

Send in Repeater with only the username changed (modifying the JWT breaks the request). The response returns the other user's private note.

![](images/api1-03-getnote-test1-note-leaked.png)

The stolen note also renders on the profile page, confirming data leakage.

![](images/api1-04-another-user-note-rendered.png)

Try `username=admin` — the admin's note contains the flag.

![](images/api1-05-admin-note-flag.png)

---

## API2:2023 — Broken Authentication

Crack the JWT signing secret offline using a wordlist attack. Using Burp's JWT Editor, forge a new token with `isAdmin: true` signed with the cracked secret.

![](images/api2-01-jwt-forged-isadmin.png)

Send `GET /api/user/user` with the forged token. Server validates the signature and returns the flag.

![](images/api2-02-broken-auth-flag.png)

---

## API3:2023 — Broken Object Property Level Authorization

Inspect `GET /api/scores` — response reveals `username` and `score` fields per user, hinting they're both stored in the same schema.

![](images/api3-01-scores-observed.png)

Capture `POST /api/register` and send to Repeater. Normal body only has `username` and `password`.

![](images/api3-02-register-normal-request.png)

Add `"score": "9999"` to the body and send. Server accepts it — registration successful.

![](images/api3-03-register-score-injected.png)

Check `/api/scores` — the new account is at the top with score 9999.

![](images/api3-04-scoreboard-9999.png)

Scroll the scores response — flag is returned at the bottom.

![](images/api3-05-scoreboard-flag.png)

---

## API4:2023 — Unrestricted Resource Consumption

Using Postman with the DVAPI collection, send a normal upload to `POST /api/profile/upload`. Small file uploads fine (251 KB, HTTP 200).

![](images/api4-01-upload-normal-success.png)

Upload a 512 MB file to the same endpoint. Server accepts it without restriction and returns the flag.

![](images/api4-02-upload-512mb-flag.png)

---

## API5:2023 — Broken Function Level Authorization

Capture a request from `/user/Charlie` in Burp. Send `OPTIONS /api/user/Charlie` — the `Allow` response header reveals `GET, HEAD, DELETE`.

![](images/api5-01-options-delete-allowed.png)

Send `DELETE /api/user/Charlie` with a standard user JWT. Server deletes the account and returns the flag.

![](images/api5-02-delete-user-flag.png)

---

## API6:2023 — Unrestricted Access to Sensitive Business Flows

Capture `POST /api/addTicket` in Burp and send to Intruder. Mark the `message` value as the payload position.

![](images/api6-01-addticket-intruder-setup.png)

Set payload type to **Null payloads**, count **500** (Sniper attack) — this sends 500 identical requests without modification.

![](images/api6-02-intruder-500-null-payloads.png)

Run the attack and inspect responses. One response returns the flag alongside `"Unrestricted Access to Sensitive Business Flows"`.

![](images/api6-03-intruder-flag-response.png)

---

## API7:2023 — Server Side Request Forgery

On the profile page, the "Update Note With Link" field fetches a URL server-side. Enter a Burp Collaborator URL and submit.

![](images/api7-01-collaborator-url-in-profile.png)

Intercept the `POST /api/addNoteWithLink` request in Burp — body contains `{"url": "<collaborator URL>"}`. Send to Repeater.

![](images/api7-02-addnotewithlink-request.png)

Server responds HTTP 200 and the fetched HTML appears in the `note` field — confirming the server made the outbound request.

![](images/api7-03-addnotewithlink-success.png)

Check Burp Collaborator. DNS and HTTP hits are received from the server's IP, confirming outbound SSRF.

![](images/api7-04-collaborator-hit.png)

Per DVAPI docs, port 8443 on localhost holds the flag. Change the URL to `http://127.0.0.1:8443/` and send.

![](images/api7-05-localhost-8443-request.png)

Server fetches the internal service and returns the flag in the `note` field of the response.

![](images/api7-06-ssrf-flag.png)

---

## API8:2023 — Security Misconfiguration

Add a note on your profile with Burp running to capture `POST /api/addNote`. Send to Repeater.

![](images/api8-02-addnote-request-captured.png)

Send `OPTIONS /api/addNote` to see what methods the endpoint accepts.

![](images/api8-03-options-allowed-methods.png)

Use the JWT Editor extension to decode the current token — payload shows `userId`, `username`, and `isAdmin: false`.

![](images/api8-04-jwt-decoded.png)

Tamper the JWT payload without re-signing (e.g., set `isAdmin: true`) and send. Server returns HTTP 401 but the error response leaks a full stack trace and the flag.

![](images/api8-05-stack-trace-flag.png)

---

## API9:2023 — Improper Inventory Management

Load the challenges page and intercept in Burp. Notice challenges are fetched via `POST /api/allChallenges` with body `{"released": 1}` — unusual to use POST with a parameter for retrieval.

![](images/api9-01-allchallenges-post-proxy.png)

Send to Repeater. Normal response returns 10 challenges.

![](images/api9-02-allchallenges-released-response.png)

Rename the parameter from `released` to `unreleased`. Server returns 2 hidden challenges — the flag is embedded in the `shortDescription` of Challenge12.

![](images/api9-03-unreleased-param-flag.png)

---

## API10:2023 — Unsafe Consumption of APIs

Send a login request with a classic SQL injection payload in the password field. Server returns HTTP 401 — Authentication failed.

![](images/api10-01-sqli-failed.png)

Try NoSQL injection — replace the password value with the MongoDB operator `{"$gt": 0}`. The query evaluates to true for any stored password. Server returns HTTP 200 and the flag.

![](images/api10-02-nosqli-flag.png)
