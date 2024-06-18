import cn from 'classnames'

import {useState, useEffect, useRef} from 'react'

import styles from './style.module.css'
import media_type from '../../configs/constants'

const FileImput = ({onChange, file = null, className, mediaType}) => {
    const [currentFile, setCurrentFile] = useState(file);
    const fileInput = useRef(null);
    const [isError, setIsError] = useState(false)
    const [errorMsg, setErrorMsg] = useState("");
    const allowedTypes = {
        video: media_type.videoTypes,
        audio: media_type.audioTypes,
        file: media_type.fileTypes
    }

    const validateFile = (file) => {
        if (!allowedTypes[mediaType].includes(file.type)) {
            setIsError(true);
            setErrorMsg(`Разрешены только файлы в формате: ${allowedTypes[mediaType]}`);
            setCurrentFile(null)
            onChange(null)
            return false
        }
        setIsError(false)
        return true
    }

    const getFile = (file) => {
        if (file) {
            onChange(file)
        }
    };

    useEffect(
        (_) => {
            if (file !== currentFile) {
                setCurrentFile(file);
            }
        },
        [file]
    );

    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return "0 Bytes";

        const k = 1024,
            dm = decimals < 0 ? 0 : decimals,
            sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
            i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    }


    return (
        <div className={cn(styles.container, className)}>
            <div className={styles.inputSection}>
                <label className={styles.label}>Выбрать файл</label>
                <input
                    id="file"
                    className={styles.fileInput}
                    type="file"
                    ref={fileInput}
                    onChange={(e) => {
                        const file = e.target.files[0]
                        if (!file) return
                        if (validateFile(file)) {
                            getFile(file);
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
                <div className={styles.title}>
                    <div>Информация по файлу:</div>
                    <table className={styles.table}>
                        <tbody>
                        <tr>
                            <td>Имя:</td>
                            <td>{currentFile.name}</td>
                        </tr>
                        <tr>
                            <td>Тип:</td>
                            <td>{currentFile.type}</td>
                        </tr>
                        <tr>
                            <td>Размер:</td>
                            <td>{formatBytes(currentFile.size)}</td>
                        </tr>
                        </tbody>
                    </table>
                </div>

            )}
        </div>
    );

}

export default FileImput;