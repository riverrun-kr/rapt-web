# Data Deletion

> This page gathers, in one place, how to remove what using Rapt leaves behind. What is stored where is set out in the [Privacy Policy](/en/privacy/).
>
> This English text is provided for the reader's convenience. The [Korean version](/data-deletion/) is the governing text.

## First: what the operator holds

Rapt has no sign-up and no sign-in, and there is no operator server holding what users write. While you use the app, the operator builds up nothing per user.

- **Inquiry emails** — If you wrote to support@rapt.kr, that email remains. Ask at the same address and it will be deleted.
- **Abuse-prevention records** — The converted address value used to count spell-check usage is deleted automatically after midnight Korea time (it stays in the database's recovery feature for up to 30 days). You do not need to ask.

What follows is how to remove things yourself, from your own devices and accounts.

## Your writing — deleting it in the app

Deleting a piece of writing in the app moves it to the **trash**. Deleting it permanently from the trash removes it from both the device and iCloud, and it disappears on your other devices signed in to the same account. Its posting record (post IDs, link, the posting account's Threads user ID, where it was split and a fingerprint, plus the text as posted for pieces posted with 1.0) is deleted with it.

## Removing everything left on your devices and in iCloud

Do it in this order.

- First tap **Disconnect Account** in the app. Threads connection information may stay in the device's keychain even after the app is deleted.
- Delete Rapt from **every device** you use. If the app stays on even one device, that device's writing may upload again after you clear iCloud.
- Last, delete Rapt's remaining data from iCloud. On iPhone: **Settings → Apple Account → iCloud → Manage Storage → Rapt → Delete**. On Mac: in System Settings, under **Apple Account → iCloud**, choose Rapt in storage management and delete it.

Files you exported yourself (zip, Markdown, text) must be deleted separately from wherever you saved them.

## Disconnecting Threads

Tapping **Disconnect Account** in the app deletes the access token, Threads user ID and username stored on your device. The operator has never held this information. The posting record kept with each posted piece (including the posting account's Threads user ID) stays on your device and in iCloud with that piece, and is deleted when you permanently delete it from the trash.

To revoke the permission on the Threads side as well, remove Rapt under **Settings → Account → Website permissions** in the Threads app.

**Rapt cannot delete posts already on Threads** — you must delete those in Threads directly.

## The relay server used by spell checking and account connection

Spell checking sends the text to check, and connecting a Threads account sends the authorization code Threads gives, to the relay server. Both happen only when you run them yourself, and the relay server does not store text, codes or tokens. Posting requests do not go through the relay; they go straight from the app to Threads.

## Error records at the spell-checking service

From November 12, 2026, Baikal AI (bareun.ai), which provides Korean spell checking, may keep the body of a failed request to diagnose the fault. It deletes that body once the review is finished, and at the latest three years after recording it. If you want it deleted sooner, write to support@rapt.kr with part of the text and the date you checked it, and the operator will ask Baikal AI to delete it.

## Other inquiries

**[support@rapt.kr](mailto:support@rapt.kr)**
