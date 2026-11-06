# Privacy Policy

> Effective 2026-11-06 · Last revised 2026-11-06
>
> This English text is provided for the reader's convenience. The [Korean version](/privacy/) is the governing text.

카인드닷츠 (KIND_DOTS, the &ldquo;operator&rdquo;) runs the Rapt app and the website rapt.kr, and handles your personal information as set out below.

## 1. Personal Information We Process

Rapt has no sign-up or sign-in, and contains no advertising or analytics SDK and no crash-reporting tool. What you write is stored on your devices and in your iCloud (section 2). The personal information the operator processes is limited to the following.

- **Email inquiries** — The email address you write from and the content of your inquiry (including attachments). Purpose: replying, and handling complaints and disputes. Legal basis: steps taken at the data subject's request (Personal Information Protection Act, Article 15(1)4). Retention: three years from the day the inquiry is resolved.
- **Spell-check relay** — The Korean text you ask to check and your connecting IP address. Purpose: providing the spell check. Legal basis: the same provision. Retention: not stored.
- **Threads connection relay** — The authorization code and access token Threads issues, your Threads user ID, and your connecting IP address. Purpose: exchanging the access token. Legal basis: the same provision. Retention: not stored.
- **Abuse prevention** — A value made by converting your connecting IP address with a secret key only the operator holds, the number of words sent that day, and the number of requests in one minute. Purpose: preventing excessive use and automated abuse. Legal basis: the operator's legitimate interests (the same Act, Article 15(1)6). Retention: the daily count until midnight Korea time; the per-minute counts for one to two minutes.

Without the key, the value used for abuse prevention cannot be turned back into the original address, and the operator neither turns it back nor links it across days. Separately, Cloudflare's rate-limiting feature counts spell-check and Threads connection requests per connecting IP address for one minute, and that count disappears after one minute.

Beyond this, the relay server keeps daily totals of requests and words by feature and result. These totals contain nothing that identifies you (no IP address, account or device information) and none of your writing.

In the App Store privacy label, &ldquo;Identifiers › Device ID&rdquo; refers to the converted address value above, and &ldquo;Usage Data › Product Interaction&rdquo; refers to the usage counts and the daily totals. &ldquo;User Content › Other User Content&rdquo; refers to the body of a check request that the spell-checking service in section 3 may keep to diagnose errors. None of this is linked to you.

## 2. Storage of What You Write

What you write in Rapt (post bodies, threads and so on) is stored on your device and **synced, through your own Apple iCloud account, to your other devices signed in to that same account.** Apple keeps and protects what is stored in iCloud, and Apple's privacy policy applies.

The operator has no server that stores your writing, and cannot access your writing, including what is in iCloud. Your writing leaves your devices and iCloud only when you yourself run one of the features in section 3.

## 3. Information That Leaves Only When You Run a Feature

**Spell checking** — The Korean text you ask to check is sent through the operator's relay server to the spell-checking service of Baikal AI, Inc. (bareun.ai). The relay server only forwards the text and does not store it, and the operator does not read it. Requests sent to Baikal AI carry nothing that identifies you (no IP address, device or account). Baikal AI's rule is not to keep the content of check requests, but from November 12, 2026 it may keep the body of a failed request in its error logs to diagnose the fault. It deletes that body once the review is finished, and at the latest three years after recording it (Baikal AI terms of use, Article 9). The relay server exists so that the access key the check requires never has to sit inside the app. Spell checking of text that is not in Korean happens on your device, and that text does not leave the device.

**Connecting a Threads account** — When you connect an account, the step that exchanges the authorization code Threads issues for an access token passes through the operator's relay server, so that the secret key this exchange requires never has to sit inside the app. The relay server only forwards the code and the token; it does not store them.

**What Rapt receives from Threads** — When you connect an account, Rapt receives your Threads user ID, your username and an access token (valid for up to 60 days; the app renews it itself), and stores them only in this device's keychain. When you publish, the post ID, link, publishing time and the text as published are stored with that piece of writing on your device and in iCloud. Tapping &ldquo;Disconnect Account&rdquo; in the app deletes the keychain information; post IDs and links are deleted when you permanently delete that writing from the trash. [Data Deletion](/en/data-deletion/) sets out how.

**Publishing to Threads** — When you publish, your writing is sent directly from the app to Threads (Meta) and posted to your account. This is a posting action you intended, and Threads (Meta) policy governs posted content. Publishing does not pass through the relay server.

## 4. Outsourced Processing

The operator entrusts the processing of personal information to the companies below. These companies must not use the information beyond the work entrusted to them, and the operator manages and supervises them, through each company's terms and data-processing conditions and its service settings, to the same level of protection as this policy.

- Gabia Inc. — keeping email inquiries (Hiworks)
- Cloudflare, Inc. — running the relay server and keeping its records (Cloudflare Workers, D1). See section 5 for transfers outside Korea
- Baikal AI, Inc. — Korean spell checking (bareun.ai)

## 5. Transfer Outside Korea

When you run a spell check or connect a Threads account, the information below is transferred to Cloudflare, which runs the relay server.

- Legal basis: outsourcing and storage needed to provide the feature you asked for (Personal Information Protection Act, Article 28-8(1)3, disclosed in this policy)
- Recipient: Cloudflare, Inc. (privacyquestions@cloudflare.com)
- Countries: requests are processed mainly in the United States (and may be processed at Cloudflare data centers in other countries, depending on the network route); records are kept in the Asia-Pacific region of Cloudflare D1
- Items: the text you ask to check; the Threads authorization code, access token and user ID; your connecting IP address; the converted address value with word and request counts
- When and how: sent over an encrypted network connection (HTTPS) each time you use one of these features
- Purpose and retention: running the relay server and preventing abuse. Text, codes, tokens and IP addresses disappear as soon as they are processed; the converted value is kept only for the period in section 6
- How to refuse, and the effect: if you do not use Korean spell checking or Threads account connection, nothing is transferred. Only those two features become unavailable; writing, copying, English spell checking and exporting all keep working.

## 6. Retention and Destruction

- Email inquiries: kept for three years from the day the inquiry is resolved, then permanently deleted from the mailbox and its trash. Once payments are introduced, records of complaints and disputes must be kept for three years under Korea's Act on the Consumer Protection in Electronic Commerce, so all inquiry records follow the same period.
- Abuse-prevention records: a cleanup job that runs every minute deletes the daily count from the database after midnight Korea time, and the per-minute counts within one to two minutes. Deleted records stay in the Cloudflare database's recovery feature for up to 30 days and then disappear.
- The operator keeps no other personal information, and makes no paper documents.

## 7. Security Measures

- All communication among the app, the relay server and outside services is encrypted with HTTPS.
- The spell-checking key, the Threads app secret and the address-conversion key are not in the app; they sit only in the relay server's secret store.
- The relay server runs with request logging turned off, and does not store text, tokens or IP addresses.
- The Threads access token is stored only in your device's keychain (this device only).
- Administrative access to the relay server and the mailbox is held by one person, the operator.

## 8. Disclosure to Third Parties

The operator does not provide or sell your personal information to third parties. The outsourcing in section 4 and the Threads publishing you run yourself are not third-party disclosure.

**Requests from public authorities** — The operator does not keep users' writing or account information, so there is little to provide even if a law enforcement agency or another public authority requests user information. If such a request arrives, the operator first checks that it rests on a legal basis and follows the required procedure (such as a warrant). If it lacks a basis or appears unlawful, the operator declines it or challenges it through the procedures the law provides. When a request must be complied with, the operator provides only the minimum necessary within its scope, and keeps a record of the requesting authority, the request, its legal basis, and the operator's response.

## 9. Cookies and Automatic Collection

The Rapt app and the website (rapt.kr) use no cookies, visit analytics or similar automatic collection. The website is served by GitHub Pages (GitHub, Inc., United States), and GitHub may record visitors' IP addresses for service security. The operator does not receive those records.

## 10. Processing Through the Apple Platform

Rapt is distributed through the Apple App Store. Apple's privacy policy separately governs any processing that occurs when you download, pay for (should payments be introduced later), or update the app through the App Store, and that processing is outside the operator's control.

## 11. Children's Personal Information

Rapt does not ask your age and does not separately collect personal information from children. If a child under 14 writes to us by email, the information is processed only as far as needed to reply.

## 12. Your Rights and How to Exercise Them

You (or your legal representative or an authorized agent) may at any time ask to see, correct or delete, or stop the processing of, the personal information the operator processes about you. Write to support@rapt.kr and you will hear the result within 10 days; if the law requires refusal, you will be told why. All the operator keeps per user is email inquiry records, and the converted address value that is deleted automatically at midnight Korea time.

You can delete writing stored in the app yourself. **Content synced to iCloud remains in iCloud after the app is deleted. It stays visible on your other devices signed in to the same account, and it comes back if you reinstall the app.** The steps for removing everything are in [Data Deletion](/en/data-deletion/).

## 13. Remedies

If you need advice or a remedy for an infringement of your personal information, you can contact the agencies below.

- Personal Information Dispute Mediation Committee: 1833-6972 (www.kopico.go.kr)
- Personal Information Infringement Report Center: 118 (privacy.kisa.or.kr)
- Supreme Prosecutors' Office: 1301 (www.spo.go.kr)
- National Police Agency: 182 (ecrm.police.go.kr)

## 14. Changes to This Policy

This policy is updated when the service or the way data is handled changes, and the changes and their effective date are posted on this page. Changes that are unfavorable to users or otherwise significant are posted at least seven days before they take effect and are also announced in the app's update notes. Earlier versions are available on request at support@rapt.kr.

## 15. Privacy Officer

For privacy inquiries, complaints and remedies, please contact:

- Privacy officer: 김재민
- Email: support@rapt.kr
