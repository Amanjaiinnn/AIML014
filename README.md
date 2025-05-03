# 🤖 AIML014: AI-Powered Request Management System

Welcome to **AIML014**, an AI/ML-driven request management system designed to streamline and automate service request handling. This project leverages the capabilities of OpenStack and Python to provide an efficient solution for managing and processing user requests.

## 🚀 Project Overview

**AIML014** is a collaborative effort aimed at developing a robust system that automates the management of service requests. By integrating OpenStack's cloud computing services with Python's versatility, the system ensures efficient handling, tracking, and resolution of user requests.

## 🧰 Features

* **Automated Request Handling**: Seamless processing of user requests with minimal manual intervention.
* **Database Integration**: Utilizes SQLite (`requests.db`) for efficient data storage and retrieval.
* **Modular Architecture**: Clean separation of concerns with dedicated modules for OpenStack interactions and utility functions.
* **Scalability**: Designed to handle increasing loads by leveraging cloud infrastructure.

## 🗂️ Project Structure

```
AIML014/
├── main.py                  # Entry point of the application
├── openstack_client.py      # Handles OpenStack API interactions
├── utils/                   # Contains utility functions
│   └── helper_functions.py  # Example utility module
├── requests.db              # SQLite database for storing requests
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables and configurations
```

## 🛠️ Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/Amanjaiinnn/AIML014.git
cd AIML014
```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a `.env` file in the root directory and add necessary configurations:
```
OPENSTACK_USERNAME=your_username
OPENSTACK_PASSWORD=your_password
OPENSTACK_PROJECT_ID=your_project_id
OPENSTACK_AUTH_URL=https://your-openstack-auth-url
```

5. **Run the Application**
```bash
python main.py
```

## 🧪 Usage

Once the application is running:
* **Submit Requests**: Users can submit service requests through the interface.
* **Track Status**: Monitor the status of submitted requests in real-time.
* **Automated Processing**: The system processes requests using predefined workflows and OpenStack services.

## 👥 Team Contributions

This project is a result of the collaborative efforts of:
* **Aman Jain**: *OpenStack Integration Specialist*
  * Oversaw the project's development and integrated OpenStack services.
* **Shreeyansh Mittal**: *OpenStack Integration Specialist and handled the LLM integration*
  * Responsible for the integration of apis.
* **Anuj Sinha**: *Utility Module Developer & Code Optimizer*
  * Created utility functions and optimized code for better performance.

## 📹 Demonstration Video

*A comprehensive walkthrough of the AIML014 system is available in the video below:*

[Watch the Demo](https://youtu.be/SCqb5lVjnLY)

*Note: Replace VIDEO_ID with your actual YouTube video ID once available.*

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
   Click on the 'Fork' button at the top right corner of this page.

2. **Create a New Branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make Your Changes**
   Implement your feature or fix.

4. **Commit Your Changes**
```bash
git commit -m "Add your message here"
```

5. **Push to Your Fork**
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
   Submit a pull request detailing your changes for review.

## 📬 Contact

For any inquiries or feedback:
* **Aman Jain**: amanjain200310@gmail.com
* **Shreeyansh Mittal**: shreeyanshmittal@gmail.com
* **Anuj Sinha**: theanujsinha@gmail.com

---

*Thank you for exploring AIML014! We hope this system enhances your service request management experience.*
