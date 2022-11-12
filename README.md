## Frappe Meta Integration

Meta Cloud API Integration for frappe framework

---

### Main Features

1. Supports Frappe Version 14
2. Supports Text, Media and Template Based WhatsApp Messaging.
3. Sends a Welcome Message on User Creation.


### Screenshots

1. Workspace

    ![Workspace](https://user-images.githubusercontent.com/91651425/201308548-63279562-6152-4cd3-94a4-29bf6df173a0.png)


2. WhatsApp Cloud API Settings

    ![WhatsApp Cloud API Settings](https://user-images.githubusercontent.com/95274912/201276165-3039a7d4-44f3-4bf2-9a04-dd27a05a0e84.png)
  
    ![token verification](https://user-images.githubusercontent.com/95274912/201276360-21a41b58-6e97-4168-a592-cea02b8fbbe4.png)


    2.1 Token Verification
    
      - Using your Facebook developer account, create the WhatsApp Business API. 
    
      - The WhatsApp Business API is used to set the Access Token, Phone Number ID, and WhatsApp Business Account ID. 
    
      - These Data is passed to WhatsApp Cloud API Settings and then saved.
    
      - Verify the token using the "Verify Token" button. A pop-up window appears on the screen.
    
      - Add the Whatsapp number and submit.
    

3. WhatsApp Communication

   ![whatsup communication](https://user-images.githubusercontent.com/95274912/201277603-d4e79b63-4e13-492f-8aa1-4172b3396cad.png)

- There are three message types available in WhatsApp communication: text, document, and template.

    3.1 Message Type : Text
    - A text field for simple text is provided here.
          
    3.2 Message Type : Document
    - Here are some fields where media information can be entered. 
          
    3.3 Message Type : Template
    - Here message templates information can be added.

---

### How to Install

1. `bench get-app https://github.com/efeone/frappe_meta_integration.git`
2. `bench setup requirements`
3. `bench build --app frappe_meta_integration`
4. `bench --site [your.site.name] install-app frappe_meta_integration`
5. `bench --site [your.site.name] migrate`

---

### Prerequisites:

- Meta for Developers Account
- WhatsApp configured in the Meta Developer Account
- Verified Business on Meta
- Verified WhatsApp Number and a Permanent Token

---


### Dependencies:

- [Frappe](https://github.com/frappe/frappe)

---

### Contributing

Will be using the same guidelines from ERPNext

1. [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

---

#### License

GNU/General Public License (see [license.txt](https://github.com/efeone/frappe_meta_integration/blob/master/license.txt))
Frappe Meta Integration code is licensed as GNU General Public License (v3)
