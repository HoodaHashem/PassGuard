<h1 align="center">PassGuard</h1>
<h2 align="center">Terminal-Tool.</h2>

PassGuard Manager is a command-line password management tool designed for users who prefer a lightweight and secure solution for managing their passwords. Built with security as a top priority, PassGuard Manager offers a robust set of features to ensure the confidentiality and integrity of user passwords.
## Screenshots

![Image Description](imgs/Screenshot from 2024-03-29 10-21-00.png)


## Installation

Install PassGuard through
```
https://github.com/Hoodahashem/PassGuard.git
```
Then activate the vertual environment through
```
source venv/bin/activate
```
Then you'r good to lunch the Program
```
python passguradcmd.py
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file
to specify your storage type **BY DEFAULT IT WILL STORE IT IN data.json FILE**

**Recomendation**
`PASSGUARD_STORAGE_TYPE=db`
to store the information in **sql-lite** database

## About Storing Informations?
PassGuard has Two main dataBases if chosed to store the informations in .json file format You will have Two files

- **data.json:** this file will store the user informations encrypted of course the data will be **(username, user_password, url, url_password)**
- **secret.json:** this file will store the key of encryption and decryption **(THE MOST IMPORTANT FILE)**

If you chosed Storing in **sql-lite** dataBase you will have Two dataBases 
- **Guard.db:** This dataBase will store the user informations encrypted of course the data will be **(username, user_password, url, url_password)**
- **Secret-Guard:** this file will store the key of encryption and decryption **(THE MOST IMPORTANT DATABASE)**
## About Features
- **End-to-End Encryption:** All user passwords are encrypted using strong encryption algorithms within the terminal environment. This ensures that passwords remain secure even if the system is compromised.
- **Master Password:** Users are prompted to create a strong master password during setup, which is used to encrypt and decrypt the password database. The master password is never stored on disk or shared with external services, enhancing security.

- **Password Generation:** PassGuard Manager includes a password generation feature, allowing users to create complex and unique passwords directly from the command line. Users can specify the length and character sets for generated passwords.

## Security Measures
- **Offline Mode:** PassGuard Manager operates entirely offline, minimizing the risk of remote attacks and ensuring that user passwords are not transmitted over the network.

- **Open Source:** The source code of PassGuard Manager is open for inspection, allowing security experts to review the implementation for potential vulnerabilities and contribute to its improvement.
## Conclusion:
PassGuard Manager offers a secure and efficient solution for managing passwords within the terminal environment. With its focus on end-to-end encryption, password generation users can trust PassGuard Manager to protect their sensitive information effectively while providing a seamless command-line experience.
## Authors

- [@Hoodahashem](https://www.github.com/Hoodahashem)


## 🚀 About Me
Coffee-fueled coder ☕️ Full-time code rocker, part-time bug slayer.🤺Turning coffee into code, bugs into features, and errors into laughter!🤣
