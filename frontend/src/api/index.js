class Api {
  constructor(url, headers) {
    this._url = url;
    this._headers = headers
  }

  checkResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res);
      }
      const func = res.status < 400 ? resolve : reject;
      res.json().then((data) => func(data));
    });
  }

  getMacLabel() {
    // Получение метки и пользователя
    return fetch(`${this._url}/maclabel/`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getCards({ page = 1, limit = 6, full_name = '' }) {
    // Все карточки
    const search = full_name ? `&search=${full_name}` : '';
    return fetch(`${this._url}/cards/?page=${page}&limit=${limit}${search}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getCard({ card_id }) {
    // Карточка
    return fetch(`${this._url}/cards/${card_id}/`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  // getPosts({ card_id, social_id=null }) {
  //   // Посты в соц сетях
  //   const social = social_id ? `?social_id=${social_id}` : ''
  //   return fetch(`${this._url}/cards/${card_id}/publications/${social}`, {
  //     method: 'GET',
  //     headers: {
  //       ...this._headers
  //     }
  //   }).then(this.checkResponse);
  // }

  getStatistics({ card_id, social_id=null }) {
    // Статистика
    const page_social_id = social_id ? `?social_id=${social_id}` : ''
    return fetch(`${this._url}/cards/${card_id}/statistics/${page_social_id}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  addSocialNetwork({ card_id, socials, source}) {
    // Добавить соц сеть в подтвержденные
    return fetch(`${this._url}/cards/${card_id}/social_network/`, {
      method: 'POST',
      headers: {
        ...this._headers
      },
      body: JSON.stringify({
        socials: socials,
        source: source,
      })
    }).then(this.checkResponse);
  }

  discardSocialNetwork({ card_id, socials, source }) {
    // Удалить соц сеть из подтвержденных
    return fetch(`${this._url}/cards/${card_id}/social_network/`, {
      method: 'DELETE',
      headers: {
        ...this._headers
      },
      body: JSON.stringify({
        socials: socials,
        source: source,
      })
    }).then(this.checkResponse);
  }

  getSocialNetworkFound({ card_id, source }) {
    // Все найденные соц сети
    const source_name = source ? `?source=${source}` : ''
    return fetch(`${this._url}/cards/${card_id}/social_network_found/${source_name}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getSocialSearch({ social_id='', username='', full_name='', source=''}) {
    // Получение метки и пользователя
    const search = social_id ? `?social_id=${social_id}` :
      username ? `?username=${username}` :
      full_name ? `?full_name=${full_name}` :
      source ? `?source=${source}` : ''
    return fetch(`${this._url}/social_search/${search}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getSocialNetworkConfirmed({ card_id, source }) {
    // Подтвержденные соц сети
    const source_name = source ? `?source=${source}` : ''
    return fetch(`${this._url}/cards/${card_id}/social_network_confirmed/${source_name}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getSmiAboutPerson({ card_id }) {
    // СМИ о персоне
    return fetch(`${this._url}/cards/${card_id}/smi_about_person/`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  deleteCard({ card_id }) {
    // Удалить карточку
    return fetch(`${this._url}/cards/${card_id}/`, {
      method: 'DELETE',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  createCard({ full_name = '', auto_collect, avatar, attrs = [] }) {
    // Создать карточку
    return fetch(`${this._url}/cards/`, {
      method: 'POST',
      headers: {
        ...this._headers
      },
      body: JSON.stringify({
        full_name,
        avatar,
        attrs,
        auto_collect
      })
    }).then(this.checkResponse);
  }

  updateCard({ full_name, card_id, avatar, auto_collect, attrs = [] }, wasImageUpdated) {
    // Обновить карточку
    return fetch(`${this._url}/cards/${card_id}/`, {
      method: 'PATCH',
      headers: {
        ...this._headers
      },
      body: JSON.stringify({
        full_name,
        id: card_id,
        avatar: wasImageUpdated ? avatar : undefined,
        attrs,
        auto_collect
      })
    }).then(this.checkResponse);
  }

  getCardAttrs({ card_id, attr_type }) {
    // Атрибуты карточки
    const attrs = attr_type ? `&attr_type=${attr_type}` : ''
    return fetch(`${this._url}/cardattrs/?card=${card_id}${attrs}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  deleteCardAttrs({ cardattr_id }) {
    // Удалить атрибут
    return fetch(`${this._url}/cardattrs/${cardattr_id}/`, {
      method: 'DELETE',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  createCardAttrs({ data }) {
    // Записать атрибут
    return fetch(`${this._url}/cardattrs/`, {
      method: 'POST',
      body: data
    }).then(this.checkResponse);
  }

  getAttrs({attr_type = ''}) {
    // Все атрибуты или фильтр по типу
    const type = attr_type ? `attr_type=${attr_type}` : ''
    return fetch(`${this._url}/attrs/?${type}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getBioModel({ cardattr_id, type }) {
    // Получить ветор по аудиозаписи
    return fetch(`${this._url}/cardattrs/${cardattr_id}/get_bio_model/?type=${type}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getWikiSearsh({keyword = ''}) {
    // Поиск карточки в elastic
    const search = keyword ? `keyword=${keyword}` : ''
    return fetch(`${this._url}/wiki_search/?${search}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getPhotoSearch({card_id}) {
    return fetch(`${this._url}/cards/${card_id}/photo_search/`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getDictorSearch({card_id}) {
    return fetch(`${this._url}/cards/${card_id}/dictor_search/`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

  getSmiSearch({ card_id, aggs, time_zone='', date_till='', date_from=''}) {
    // Поиск карточки в elastic
    // return fetch(`http://pao.ss/pao_api/fts/search/}`, {
    const time = time_zone ? `&time_zone=${time_zone}` : ''
    const till = date_till ? `&date_till=${date_till}` : ''
    const from = date_from ? `&date_from=${date_from}` : ''
    return fetch(`${this._url}/cards/${card_id}/smi_search/?with_aggs=${aggs}${time}${till}${from}`, {
      method: 'GET',
      headers: {
        ...this._headers
      },
    }).then(this.checkResponse);
  }

  getScsSearch({ card_id, social_id, aggs}) {
    // Поиск карточки в elastic
    const social = social_id ? `&social_id=${social_id}` : ''
      return fetch(`${this._url}/cards/${card_id}/scs_search/?with_aggs=${aggs}${social}`, {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse);
  }

 /* getLangsNames() {
    // Запрос на языки
    return fetch('/pao_api/fts/get_langs/', {
      method: 'GET',
      headers: {
        ...this._headers
      }
    }).then(this.checkResponse)
        .catch(err => console.log('Ошибка при получении языков с сервера:', err))
  }*/
  getLangsNames() {
    return fetch('/pao_api/fts/get_langs/', {
      method: 'GET',
      headers: {
        ...this._headers
      }
    })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
          }
          return response.json();
        })
        .catch(error => console.log('Ошибка при получении языков с сервера:', error));
  }

}
const API_URL = '/fpk_api'
const api = new Api(process.env.API_URL || API_URL, {
  'content-type': 'application/json'
});

export default api;
