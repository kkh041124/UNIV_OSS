import React, { useState } from "react";
import styles from "./ImageSelector.module.css";
import img144 from "./secure/144px.png";
import img240 from "./secure/240px.png";
import img480 from "./secure/480px.png";
import img720 from "./secure/720px.png";
import img1080 from "./secure/1080px.png";

function ImageSelector() {
  const [image, setImage] = useState("");
  const [message, setMessage] = useState("");

  const handleImageChange = (resolution) => {
    switch (resolution) {
      case "144px":
        setImage(img144);
        setMessage("");
        break;
      case "240px":
        setImage(img240);
        setMessage("");
        break;
      case "480px":
        setImage(img480);
        setMessage("");
        break;
      case "720px":
        setImage(img720);
        setMessage("");
        break;
      case "1080px":
        setImage(img1080);
        setMessage("It’s You! (Thk Professional)");
        break;
      default:
        setImage("");
        setMessage("");
    }
  };

  return (
    <div className={styles.container}>
      <h1>Image Resolution Selector</h1>
      {image && <img src={image} alt="Selected" className={styles.preview} />}
      {message && <p className={styles.message}>{message}</p>}
      <div className={styles.buttonContainer}>
        {["144px", "240px", "480px", "720px", "1080px"].map((res) => (
          <button
            key={res}
            className={styles.resButton}
            onClick={() => handleImageChange(res)}
          >
            {res}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ImageSelector;
