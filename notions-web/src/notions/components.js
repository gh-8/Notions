import React, { useEffect, useState } from "react";

import { loadNotions } from "../lookup";

export function NotionsList(props) {
  const [notions, setNotions] = useState([]);
  useEffect(() => {
    const myCallback = (response, status) => {
      if (status === 200) {
        setNotions(response);
      } else {
        console.log("There was an error");
      }
    };
    loadNotions(myCallback);
  }, []);

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
  const className = props.className
    ? props.className
    : "btn btn-primary btn-sm";
  return action.type === "like" ? (
    <button className={className}> +{notion.id} Likes</button>
  ) : null;
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
        <ActionBtn notion={notion} action={{ type: "like" }} />
        <ActionBtn notion={notion} action={{ type: "unlike" }} />
      </div>
    </div>
  );
}
