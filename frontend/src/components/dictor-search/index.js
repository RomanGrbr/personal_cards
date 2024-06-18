import React, {useEffect, useState} from 'react'
import {useParams, useNavigate} from 'react-router-dom'

import {SmiCard} from '../../components'
import styles from './style.module.css'
import api from '../../api'

const DictorSearch = ({langs}) => {
    const {id} = useParams()
    const navigate = useNavigate()
    const [dictorSearch, setDictorSearch] = useState([])
    const [isLoading, setIsLoading] = useState(true);

    useEffect((_) => {
    api
      .getDictorSearch({ card_id: id })
      .then((res) => {
        setDictorSearch(res.result)
        setIsLoading(false);
        })
      .catch((err) => {
        setIsLoading(false);
        navigate(`/fpk/${id}`);
      })
    }, [])

    return (
        <div>
            {isLoading && <div className={styles.loader}></div>}
            {dictorSearch && dictorSearch.map((item) => (
                <SmiCard item={item} langs={langs} key={item.article_uuid}/>
            ))}
        </div>
    )
}

export default DictorSearch;
