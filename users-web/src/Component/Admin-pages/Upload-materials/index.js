import react, { Component } from "react";
import Navbar from "../Navbar/index";
import { Form, Button, Modal } from 'react-bootstrap';
import CourseNav from "../Course-Nav/index";
import "./style.css";

class UploadMaterials extends Component {

    state = {
        show: false,
    }
    handleClose = () => {
        this.setState({
            show: false
        })
    };
    handleShow = () => {
        this.setState({
            show: true
        })
    };


    //HANDEL UPLOAD MATERIALS
    handelFileUpload = (e) => {
        e.preventDefault();
        const file = document.getElementById("myFile").value;
        const fileDesc = document.getElementById('exampleForm.ControlTextarea1').value;
        //GET USERNAME FROM LOCALSTORAGE
        let userInfo = localStorage.getItem("userInfo");
        userInfo = JSON.parse(userInfo);

        //GET COURSE CODE FROM LOCALSTORAGE
        let code = localStorage.getItem("code")

        //HANDEL REQUEST
        const request = new XMLHttpRequest();
        const csrftoken = this.getCookie('csrftoken');

        request.open("POST", `http://127.0.0.1:8000/api/upload-material/${userInfo.username}/${code}/`);

        request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        request.setRequestHeader("X-CSRFToken", csrftoken);


        request.onload = () => {
            const response = JSON.parse(request.responseText);
            console.log(response)
        }
        const data = new FormData();
        data.append("file", file);
        data.append("description", fileDesc);

        request.send(data);
        return false;

    }
    getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }




    render() {

        return (
            <div>
                <Navbar />
                <CourseNav />
                <div className="start-page">
                    <img src="/image/upload-1.jpg" className="img-fluid" />
                    <p>You haven't uploaded any items yet ,, upload now ...</p>
                    <span onClick={this.handleShow} >Click to Upload</span>

                    {/*CREATE MATERIALS POP UP FORM TO GET DATA */}

                    <Modal show={this.state.show} onHide={this.handleClose} centered keyboard={false} className="pop-parent" >
                        <Modal.Header closeButton className="pop-header">
                            <Modal.Title>Upload Materials</Modal.Title>
                        </Modal.Header>


                        <form onSubmit={this.handelFileUpload} encType="multipart/form-data">
                            <Modal.Body className="pop-body" >
                                <Form.Label>Select File</Form.Label>
                                <br />
                                <input className="inputFile" type="file" placeholder="FILE...." id="myFile" />

                                <Form.Group controlId="exampleForm.ControlTextarea1">
                                    <Form.Label>TYPE DESC....</Form.Label>
                                    <Form.Control as="textarea" rows={3} />
                                </Form.Group>


                            </Modal.Body>
                            <Modal.Footer className="pop-footer">
                                <Button type="submit" onClick={this.handleClose} >
                                    Upload
                                </Button>
                            </Modal.Footer>
                        </form>


                    </Modal>



                </div>
            </div >
        )
    }
}

export default UploadMaterials;