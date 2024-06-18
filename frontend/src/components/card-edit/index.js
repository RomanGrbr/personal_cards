import { v4 as uuid } from 'uuid'

import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import styles from './style.module.css'
import { Button, Input, Form, ImageInput, AttrInput } from '../../components'
import api from '../../api'
import media_type from '../../configs/constants'
import AsyncSelect from "react-select/async";

const CardEdit = ({ setRead }) => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [cardFullName, setCardFullName] = useState('')
  const [cardAvatar, setCardAvatar] = useState(null)
  const [attrs, setAttrs] = useState([])
  const [fields, setFields] = useState([])
  const [autoCollect, setAutoCollect] = useState(null)
  const [confirmScs, setConfirmScs] = useState(null)
  const [cardsFileWasManuallyChanged, setCardFileWasManuallyChanged] = useState(false)
  const {image, audio, video, file} = media_type

  const getStrAttrs = ({ attrs }) => {
    let data = [];
    for (let i = 0; i < attrs.length; i++) {
      if (![image, audio, video, file].includes(attrs[i].attr_type)) {
        attrs[i]['id'] = attrs[i]['attribute']
        data.push(attrs[i]);
      }
    }
    setAttrs(data);
  };

  const checkIfDisabled = () => {
    return cardFullName === '' || cardAvatar === '' || cardAvatar === null
  }

  const delCard = () => {
    api.deleteCard({ card_id: id }).then((res) => {
      navigate(`/fpk/`)
    })
  }

  const handleChangeAutoCollect = () => {
    setAutoCollect(!autoCollect);
  };

  useEffect((_) => {
    api
      .getCard({
        card_id: id
      })
      .then((res) => {
        setCardFullName(res.full_name)
        setCardAvatar(res.avatar)
        setAutoCollect(res.auto_collect)
        setConfirmScs(res.confirm_scs)
      })
      .catch((err) => {
        navigate('/fpk');
      });
  }, []);

  useEffect(_ => {
    api
    .getAttrs({attr_type: ''})
    .then((res) => {
      setFields(
        res.results.filter(
          attr => ![image, audio, video, file].includes(
            attr.attr_type)
            )
          )
      });
  }, [])

  useEffect(_ => {
    api
      .getCardAttrs({ card_id: id })
      .then((res) => {
        getStrAttrs({ attrs: res.results });
      })
      .catch((err) => {
        navigate('/fpk');
      });
  }, [])

  const onSubmitClickHandler = (e) => {
    e.preventDefault();
    const data = {
      full_name: cardFullName,
      card_id: id,
      avatar: cardAvatar,
      auto_collect: autoCollect,
      attrs: attrs.map(item => ({
        id: item.id,
        value: item.value
      })),
    };
    api
        .updateCard(data, cardsFileWasManuallyChanged)
        .then(res => {
          setRead(true)
        })
        .catch((err) => {
          const { non_field_errors } = err;
          if (non_field_errors) {
            return alert(non_field_errors.join(', '));

          }
          const errors = Object.values(err);
          if (errors) {
            alert(errors.join(', '));
          }
        });
  }

  const onChangeNameClickHandler = (e) => {
    const value = e.target.value;
    setCardFullName(value);
  }

  const onChangeFileClickHandler = (file) => {
    setCardFileWasManuallyChanged(true);
    setCardAvatar(file)
  }

  return (

      <div className={styles.editCardForm}>
        <div title="Введите ФИО">
          <input type="text"
                 placeholder="Наименование объекта (ФИО)"
                 name="name"
                 onChange={onChangeNameClickHandler}
                 value={cardFullName} className={styles.formElement}/>
        </div>
        <div>
          {fields.map(attr => <AttrInput
              className={styles.formElement}
              key={uuid()}
              attr={attr}
              cardAttrs={attrs}
              setCardAttrs={setAttrs}
          />)}
        </div>
        <div className={styles.formElement}>
          <ImageInput
              onChange={onChangeFileClickHandler}
              label="Загрузить фото"
              file={cardAvatar}
          />
        </div>
        <div title="Автоматический сбор работает только в случае отсутствия подтвержденных социальных сетей"
             className="custom-control custom-checkbox">
          <input
              style={{width: '20px', height: '20px', marginRight: '10px'}}
              type="checkbox"
              className="custom-control-input"
              id="auto_collect"
              onChange={handleChangeAutoCollect}
              checked={autoCollect}
              disabled={confirmScs}>
          </input>
          <label className="custom-control-label" htmlFor="customCheck1">Автоматический сбор</label>
        </div>
        <Button
            title="Удалить карточку персоны"
            className="btn btn-danger col-3 mt-4"
            clickHandler={(_) => delCard({ id: id })}>
          Удалить
        </Button>
        <Button
            title="Сохранить изменения в карточке персоны"
            clickHandler={onSubmitClickHandler}
            disabled={checkIfDisabled()}
            className="btn btn-success col-3 mt-4">
          Сохранить
        </Button>
      </div>
  )
}

export default CardEdit

