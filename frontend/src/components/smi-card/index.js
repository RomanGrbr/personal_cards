import styles from './style.module.css'

const SmiCard = ({item, langs}) => {
    let date = new Date(item.sort_date * 1000);
    let formattedTime = date.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    })

    return (
        <>
            <style>
                {`
                 .searched_word {
                 background-color: #ff9; 
                    font-weight: bold; 
                 }
             `}
            </style>
            <div className={styles.smi}>
                
                    <div className={styles.header}>
                        <span> {item.domain.domain}</span>
                        <span>{(item.domain.domain !== item.domain.title && item.domain.title) && " " + item.domain.title}</span>
                    </div>

                <div className={styles.body}>
                    <div>
                        {item.media && item.media.type === 'image' ? 
                        <img src={item.media.internalUrl} className={styles.card__image}></img> : ''}
                        {item.media && item.media.type === 'video' ? 
                        <video src={item.media.internalUrl} className={styles.card__image} controls></video> : ''}
                    </div>

                    <div>
                    <div className={styles.title}><a href={`/pao/newPAO/storunit.html?article_uuid=${item.article_uuid}&index_type=${item.index_type}`}
                           className={styles.link}>
                            {item.title}
                        </a></div>
                    <span dangerouslySetInnerHTML={{ __html: item.cnt }}></span>

                    <div><span className={styles.text_muted}>Дата публикации: </span>{formattedTime}</div>
                    <div><span className={styles.text_muted}>Источник: </span><span>{item.domain.domain}</span></div>
                    <div><span
                        className={styles.text_muted}>Язык: </span> {langs[item.lang] ? langs[item.lang] : item.lang}
                    </div>
                    <div>
                        <span className={styles.text_muted}>URL: </span>
                            {item.url}
                    </div>
                    </div>
                </div>
            </div>
        </>


    )
}

export default SmiCard;