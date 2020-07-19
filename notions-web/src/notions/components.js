import React, { useEffect, useState } from "react";

import { loadNotions } from "../lookup";
//import { NotionsList } from ".";

export function NotionsComponent(props) {
  const textAreaRef = React.createRef();
  const [newNotions, setNewNotions] = useState([]);
  const handleSubmit = event => {
    event.preventDefault();
    const newVal = textAreaRef.current.value;
    let tempNewNotions = [...newNotions];
    tempNewNotions.unshift({
      content: newVal,
      likes: 0,
      id: 1234
    });
    setNewNotions(tempNewNotions);
    textAreaRef.current.value = "";
  };
  return (
    <div className={props.className}>
      <div className="col-12 mb-3">
        <form onSubmit={handleSubmit}>
          <textarea
            ref={textAreaRef}
            required={true}
            className="form-control"
            placeholder="Post a notion"
            name="notion"
          ></textarea>
          <button type="submit" className="btn btn-primary my-3">
            Notionize
          </button>
        </form>
      </div>
      <NotionsList newNotions={newNotions} />
    </div>
  );
}

export function NotionsList(props) {
  const [notionsInit, setNotionsInit] = useState([]);
  const [notions, setNotions] = useState([]);
  const [notionsDidSet, setNotionsDidSet] = useState(false);
  useEffect(() => {
    const final = [...props.newNotions].concat(notionsInit);
    if (final.length !== notions.length) {
      setNotions(final);
    }
  }, [props.newNotions, notions, notionsInit]);

  useEffect(() => {
    if (notionsDidSet === false) {
      const myCallback = (response, status) => {
        if (status === 200) {
          setNotionsInit(response);
          setNotionsDidSet(true);
        } else {
          console.log("There was an error");
        }
      };
      loadNotions(myCallback);
    }
  }, [notionsInit, notionsDidSet, setNotionsDidSet]);

  return notions.map((item, index) => {
    return (
      <Notion
        notion={item}
        className="my-5 py-5 border bg-white text-dark"
        key={`${index}-{item.id}`}
      />
    );
  });
}

export function ActionBtn(props) {
  const { notion, action } = props;
  const [likes, setLikes] = useState(notion.likes ? notion.likes : 0);
  const [userLike, setUserLike] = useState(
    notion.userLike === true ? true : false
  );
  const className = props.className
    ? props.className
    : "btn btn-primary btn-sm";

  const actionDisplay = action.display ? action.display : "Action";
  const handleClick = event => {
    event.preventDefault();
    if (action.type === "like") {
      if (userLike === true) {
        setLikes(likes - 1);
        setUserLike(false);
      } else {
        setLikes(notion.likes + 1);
        setUserLike(true);
      }
    }
  };
  const display =
    action.type === "like" ? `${likes} ${actionDisplay}` : actionDisplay;
  return (
    <button className={className} onClick={handleClick}>
      {display}
    </button>
  );
}

export function Notion(props) {
  const { notion } = props;
  const className = props.className
    ? props.className
    : "col-10 mx-auto col-md-6";
  return (
    <div className={className}>
      <p>
        {notion.id} - {notion.content}
      </p>
      <div className="btn btn-group">
        <ActionBtn
          notion={notion}
          action={{ type: "like", display: "Likes" }}
        />
        <ActionBtn
          notion={notion}
          action={{ type: "unlike", display: "Unlike" }}
        />
        <ActionBtn
          notion={notion}
          action={{ type: "share", display: "Share" }}
        />
      </div>
    </div>
  );
}
