import { v4 as uuid } from 'uuid'

import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import styles from './style.module.css'
import { Button, FileImput, Form, ImageInput } from '..'
import api from '../../api'
import media_type from '../../configs/constants'

const Media = () => {
  const {image, audio, video, file} = media_type
  const history = useNavigate()
  const { id } = useParams()
  const [mediaType, setMediaType] = useState(image)
  const [media, setMedia] = useState([])
  const [mediaTypeID, setMediaTypeID] = useState(null)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [socialImage, setSocialImage] = useState([])

  const getSocialImage = () => {
    api.getSocialNetworkConfirmed({ card_id: id }).then((res) => {
      let data = [];
      for (let i = 0; i < res.pages.length; i++) {
          data.push(res.pages[i].profilePicture.internalUrl)
      }
      setSocialImage(data);
    })
  }

  const getMedia = ({ type }) => {
    api.getCardAttrs({ card_id: id, attr_type: type }).then((res) => {
      setMedia(res.results)
      setMediaType(type)
    })
  }

  const deleteAttr = ({ id, type }) => {
    api.deleteCardAttrs({ cardattr_id: id }).then((res) => {
      getMedia({ type: type })
    })
  }

  const getAttrsType = ({ type }) => {
    api.getAttrs({attr_type: type}).then((res) => {
      if (res.results.length > 0) {
        setMediaTypeID(res.results[0].id)
      }
    })
  }

  const getBio = ({ id, type }) => {
    api.getBioModel({ cardattr_id: id, type: type }).then((res) => {
      getMedia({ type: type })
      alert(res.message);
    })
  }

  const checkIfDisabled = () => {
    return uploadedFile === null || mediaTypeID === null
  }

  let buttons = [
    {
      title: 'Фотографии',
      click: () => {
        setMediaType(image),
        setUploadedFile(null),
        getMedia({type: image})
      },
      disabled: false,
      isActive: mediaType === image,
      help: 'Перейти во вкладку добавления фотографий для персоны'
    },
    {
      title: 'Аудио',
      click: () => {
        setMediaType(audio),
        setUploadedFile(null),
        getMedia({type: audio})
      },
      disabled: false,
      isActive: mediaType === audio,
      help: 'Перейти во вкладку добавления аудиофайлов для персоны'
    },
    {
      title: 'Видео',
      click: () => {
        setMediaType(video),
        setUploadedFile(null),
        getMedia({type: video})
      },
      disabled: false,
      isActive: mediaType === video,
      help: 'Перейти во вкладку добавления видеофайлов для персоны'
    },
    // {
    //   title: 'Файлы',
    //   click: () => {
    //     setMediaType(file),
    //     setUploadedFile(null),
    //     getMedia({type: file})
    //   },
    //   disabled: false,
    //   isActive: mediaType === file,
    //   help: 'Перейти во вкладку добавления прочих файлов для персоны'
    // }
  ];

  const handleFileUpload = async () => {
    const data = new FormData()
    data.append("value", uploadedFile)
    data.append("card", id)
    data.append("attribute", mediaTypeID)

    api.createCardAttrs({data: data})
    .then((res) => {
        setUploadedFile(null)
        getMedia({ type: mediaType })
    })
    .catch((err) => {
    const { non_field_errors } = err
    if (non_field_errors) {
        return alert(non_field_errors.join(', '))
    }
    const errors = Object.values(err)
    if (errors) {
        alert(errors.join(', '))
    }
    })
  }

  useEffect(() => {
    document.title = 'Медиафайлы';
  }, []);

  useEffect((_) => {
    api
      .getCardAttrs({ card_id: id, attr_type: mediaType })
      .then((res) => {
        setMedia(res.results);
      })
      .catch((err) => {
        history('/fpk/');
      })
    getSocialImage()
  }, [])

  const disabled = checkIfDisabled();

  return (
    <div>
      <div className={styles.container}>
        {buttons.map((button) => (
            <Button
                title={button.isActive ? "" : button.help}
                className={`btn btn-outline-info ${button.isActive ? 'active' : ''} m-2`}
                key={button.title}
                clickHandler={(_) => {
                  button.click();
                }}
                disabled={button.disabled}
                isActive={button.isActive}>
              {button.title}
            </Button>
        ))}
      </div>
      <div className={styles.left}>
        <Form 
            className={styles.form}
            onSubmit={(e) => {
                e.preventDefault()
                handleFileUpload()
            }}
          >
          {mediaType === image ? 
            <ImageInput
              onChange={(file) => {
                  setUploadedFile(file)
                  getAttrsType({type: mediaType})
              }}
              className={styles.fileInput}
              label="Выбрать файл"
              file={uploadedFile}
              /> : <FileImput
              onChange={(file) => {
                setUploadedFile(file)
                getAttrsType({type: mediaType})
            }}
              className={styles.fileInput}
              file={uploadedFile}
              mediaType={mediaType}
            />}
          <Button
              title= "Добавить файл в карточку персоны"
              disabled={disabled}
              className="btn btn-success col-3">
            Добавить
          </Button>

        </Form>
        <div style={{marginRight: "50px"}}>
          {media.map((item) => (
              <ul key={uuid()}>
                {' '}
                {mediaType === image && <>
                  <img src={item.value} alt={item.value} className={styles.card__image}/><br></br>
                </>}
                {mediaType === video && <>
                  <video src={item.value} width="720" height="576" controls/><br></br>
                </>}
                {mediaType === audio && <>
                  <audio src={item.value} controls/><br></br>
                </>}
                {mediaType === file && <>
                  <a href={item.value} download>{item.value.split('/').pop()}</a><br></br>
                </>}
                <Button
                    title={item.confirmed ? 'Снять подтверждение соответствия файла к персоне': 'Подтвердить соответствия файла к персоне'}
                    key={item.label}
                    clickHandler={(_) => {
                      getBio({id: item.id, type: mediaType })
                    }}
                    className={`${item.confirmed ? 'btn btn-danger': 'btn btn-success'} m-2 `}
                >
                  {item.confirmed ? 'Снять подтверждение': 'Подтвердить'}
                </Button>

                <Button
                    title="Удалить файл из карточки персоны"
                    key={item.label}
                    clickHandler={(_) => {
                      deleteAttr({id: item.id, type: mediaType})
                    }}
                    className='btn btn-danger'
                >
                  Удалить
                </Button>
              </ul>
          ))}
          {mediaType === image && <h3>Собранные с соцсетей:</h3>}
          {mediaType === image && socialImage.map((image) =>
              // <li><img src={image} className={styles.card__image}/></li>
              <ul>{image}</ul>
          )}
        </div>

      </div>
    </div>

  );
};

export default Media
