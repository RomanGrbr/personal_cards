import React, {useEffect, useState} from 'react'

import {
    Card,
    CardList,
    Container,
    Main,
    Pagination,
    CardCreate
} from '../../components';
import styles from './styles.module.css';
import {useCards} from '../../utils/index.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import {InputGroup, Form, Button} from "react-bootstrap";
import {faXmark} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const HomePage = () => {
    const {cards, getCards, cardsCount, cardsPage, setCardsPage} = useCards()
    const [searchFullName, setSearchFullName] = useState('')
    const [formVisiblity, setFormVisiblity] = useState(false)

    useEffect(() => {
        document.title = 'ФПК';
    }, []);

    useEffect(
        (_) => {
            getCards({page: cardsPage});
        },
        [cardsPage]
    );

    const newCardClickHandler = (_) => formVisiblity ? setFormVisiblity(false) : setFormVisiblity(true)
    const onSubmitClickHandler = (e) => {
        e.preventDefault();
        getCards({full_name: searchFullName});
    }
    const deleteClickHandler = () => setSearchFullName('');

    const onChangeClickHandler = (e) => {
        const value = e.target.value;
        setSearchFullName(value);
    }
    const onMouseOverHandler = (e) => e.target.style.backgroundColor = '#2c3e50'
    const onMouseOutHandler = (e) => e.target.style.backgroundColor = '#34495e'
    const onPageChangeClickHandler = (page) => setCardsPage(page)

    return (
        <Main>
            <Container>
                <div style={{display: 'flex', justifyContent: 'space-between', paddingTop: '8px'}}>
                    <div style={{display: 'flex', flexDirection: 'column'}}>
                        <Button
                            title="Добавить новую карточку"
                            onClick={newCardClickHandler}
                            className="mb-5"
                            style={{backgroundColor: '#2c3e50', color: 'white', border: 'none', width: '140px', fontSize: '15px'}}
                            onMouseOver={onMouseOverHandler}
                            onMouseOut={onMouseOutHandler}
                            isActive={formVisiblity}
                        >

                            Новая карточка
                        </Button>
                        {formVisiblity && <CardCreate/>}
                    </div>
                    <form onSubmit={onSubmitClickHandler} className='col-5'>
                        <InputGroup className="mb-1">
                            <Button title="Очистить поле" onClick={deleteClickHandler} className="btn btn-secondary"><FontAwesomeIcon icon={faXmark} /></Button>
                            <Form.Control onChange={onChangeClickHandler} value={searchFullName}/>
                            <Button
                                title="Выполнить поиск уже существующих карточек"
                                type="submit"
                                style={{backgroundColor: '#2c3e50', color: 'white', border: 'none', fontSize: '15px'}}
                                onMouseOver={onMouseOverHandler}
                                onMouseOut={onMouseOutHandler}>
                                Искать
                            </Button>
                        </InputGroup>
                    </form>
                </div>



                <Pagination
                    count={cardsCount}
                    limit={10}
                    page={cardsPage}
                    onPageChange={onPageChangeClickHandler}
                />
                <CardList>
                    {cards.map((card) => (
                        <Card {...card}
                              name={card.full_name}
                              avatar={card.avatar}
                              key={card.id.toString()}/>
                    ))}
                </CardList>
            </Container>
        </Main>
    );
};

export default HomePage;
