import {v4 as uuid} from 'uuid'

import {useEffect, useState} from 'react'

import styles from './style.module.css'
import {Input, Textarea} from '../../components'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPencil, faTrash} from "@fortawesome/free-solid-svg-icons";




const AttrInput = ({attr, cardAttrs, setCardAttrs}) => {
    const [attrValue, setAttrValue] = useState({
        id: null,
        is_uniq: attr.is_uniq, //заменил
        label: '',
        value: ''
    })
    const [may, setMay] = useState(true)

    const [editingAttr, setEditingAttr] = useState(null);
    const [editingDate, setEditingDate] = useState(false);
    const [isButtonDisabled, setIsButtonDisabled] = useState(false);

    const [editing, setEditing] = useState(false)



    const handleEditClick = (item) => {
        setEditingAttr(item);
        setEditingDate(true)
        setAttrValue({
            id: item.id,
            is_uniq: item.is_uniq, //заменил
            label: item.label,
            value: item.value
        });
    }

    const handleValueChange = (e) => {

        const value = e.target.value;
        setAttrValue(prev => ({
            id: attr.id,
            is_uniq: attr.is_uniq, //заменил
            label: attr.label,
            value: value
        }))
        setEditingDate(true);
    }
    /*const handleAddClick = _ => {
        if (attrValue.value === '' || !attrValue.id) return;
        if (editingAttr) {
            setCardAttrs(cardAttrs.map(attr => attr.value === editingAttr.value ? attrValue : attr));
            setEditingAttr(null);
            setEditingDate(false)
        } else {
            setCardAttrs([...cardAttrs, attrValue]);
        }
        setAttrValue({
            id: null,
            is_uniq: false,
            label: '',
            value: ''
        });
        if (attr.is_uniq) setMay(false);
    }*/

    const handleAddClick = _ => {
        if (attrValue.value === '' || !attrValue.id) return;
        if (!editingAttr && attr.is_uniq && cardAttrs.some(attr => attr.label === attrValue.label)) return;

        if (editingAttr) {
            setCardAttrs(cardAttrs.map(attr => {
                if (attr.value === editingAttr.value) { //заменил
                    return attrValue;
                }
                return attr;
            }));
            setEditingAttr(null);
            setEditingDate(false)
            setEditing(false)
        } else {
            setCardAttrs([...cardAttrs, attrValue]);
        }

        setAttrValue({
            id: null,
            is_uniq: attr.is_uniq, //заменил
            label: '',
            value: ''
        });
        if (attr.is_uniq) setMay(false);

    };

    useEffect(() => {
        const isNotUniq = attrValue.is_uniq && !editingAttr && cardAttrs.some(attr => attr.label === attrValue.label);
        setIsButtonDisabled(!attrValue.value || (!editingAttr && isNotUniq));
    }, [attrValue.value, attrValue.label, attrValue.is_uniq, cardAttrs, editingAttr]);




    const getTypeInput = () => {
        if (attr.attr_type !== 'string') {
            return <Input
                label={attr.label}
                type={attr.attr_type}
                name={attr.field_name}
                placeholder={attr.help_text}
                onChange={(e) => {
                    handleValueChange(e)
                }}
                value={attrValue.value}
            />
        } else {
            return <Textarea
                name={attr.field_name}
                label={attr.label}
                placeholder={attr.help_text}
                onChange={(e) => {
                    handleValueChange(e)
                }}
                value={attrValue.value}
            />
        }
    }

    return (
        <div className="d-flex justify-content-between mt-3">
            <div className="w-75">
                {getTypeInput()}
                <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                    {cardAttrs.map(item => {
                        if (attr.label === item.label) {
                            return (
                                <div key={uuid()} style={{ display: 'flex', margin: '10px' }}>
                                    <div className="input-group">
                                    <span style={{
                                    display: 'inline-block',
                                    padding: '5px',
                                    border: '1px solid #6C757D',
                                    borderRadius: '5px 0 0 5px',
                                    backgroundColor: "#FFFFFF",
                                    }}>{item.value}
                                    </span>
                                    <button
                                        style={{zIndex: 0}}
                                        title="Редактировать информацию в карточке"
                                        className="btn btn-outline-secondary"
                                        onClick={() => {
                                            handleEditClick(item)
                                            setEditing(true)
                                        }}>
                                        <FontAwesomeIcon icon={faPencil} />
                                    </button>
                                    <button
                                        disabled={editing}
                                        style={{zIndex: 0}}
                                        title="Удалить информацию из карточки"
                                        className="btn btn-outline-secondary"
                                        onClick={_ => {
                                            const cardAttrsUpdated = cardAttrs.filter(attr => attr.value !== item.value);
                                            setCardAttrs(cardAttrsUpdated);
                                            if (!may) {
                                                setMay(true);
                                            }
                                        }}>
                                        <FontAwesomeIcon icon={faTrash}/>
                                    </button>
                                </div>
                                </div>
                            );
                        }
                    })}
                </div>
            </div>
            <div className="w-30">
               {/* { (may || editingDate) &&
                    <button
                        title={'Добавить информацию в карточку'}
                        className="btn btn-success mr-3"
                        style={{minHeight: '50px'}}
                        onClick={handleAddClick}
                        disabled={isButtonDisabled}>
                        {editingAttr ? 'Сохранить изменения' : 'Добавить'}
                    </button>
                }*/}
                {may && !editingAttr &&
                    <button
                        title={'Добавить информацию в карточку'}
                        className="btn btn-success mr-3"
                        style={{minHeight: '50px'}}
                        onClick={handleAddClick}
                        disabled={isButtonDisabled}>
                        Добавить
                    </button>
                }

                {editingAttr &&
                    <button
                        title={'Сохранить изменения'}
                        className="btn btn-success mr-3"
                        style={{minHeight: '50px'}}
                        onClick={handleAddClick}
                        disabled={isButtonDisabled}>
                        Сохранить изменения
                    </button>
                }

            </div>
        </div>
    )
}

export default AttrInput;