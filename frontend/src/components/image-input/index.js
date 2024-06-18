import cn from 'classnames'

import { useState, useEffect, useRef } from 'react'

import styles from './style.module.css'
import media_type from '../../configs/constants'

const ImageInput = ({ label, onChange, file = null, className}) => {
  const [currentFile, setCurrentFile] = useState(file);
  const fileInput = useRef(null);
  const allowedTypes = media_type.imageTypes
  const [isError, setIsError] = useState(false)
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(
    (_) => {
      if (file !== currentFile) {
        setCurrentFile(file);
      }
    },
    [file]
  );

  const validateFile = (file) => {
    if (!allowedTypes.includes(file.type)) {
      setIsError(true);
      setErrorMsg(`Разрешены только файлы в формате: ${allowedTypes}`);
      setCurrentFile(null);
      onChange(null)
      return false
    }
    setIsError(false);
    return true
  }

  const getBase64 = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      setCurrentFile(reader.result);
      onChange(reader.result);
    };
    reader.onerror = function (error) {
      console.log('Error: ', error);
    };
    };

    return  (
        <div className={cn(styles.container, className)}>
            <div className={styles.inputSection}>
                <label className={styles.label}>{label}</label>
                <input
                    className={styles.fileInput}
                    type="file"
                    ref={fileInput}
                    onChange={(e) => {
                        const file = e.target.files[0];
                        if (!file) return
                        if (validateFile(file)) {
                            getBase64(file);
                        }
                    }}
                />

                <div
                    onClick={(_) => {
                        fileInput.current.click();
                    }}
                    className={styles.button}
                    type="button"
                >
                    Выбрать файл
                </div>
            </div>
            {isError && <div className="error-text">{errorMsg}</div>}
            {currentFile && (
                <div
                    className={styles.image}
                    style={{
                        backgroundImage: `url(${currentFile})`
                    }}
                />
            )}
        </div>
    )

}

export default ImageInput;
