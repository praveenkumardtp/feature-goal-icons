import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Picker, EmojiData } from "emoji-mart";
import "emoji-mart/css/emoji-mart.css";

import { RootState } from "../store";
import { addGoal, updateGoalIcon } from "../store/goalsSlice";

interface Goal {
  id: string;
  title: string;
  completed: boolean;
  icon?: string;
}

const GoalManager: React.FC = () => {
  const dispatch = useDispatch();
  const goals: Goal[] = useSelector((state: RootState) => state.goals);

  const [title, setTitle] = useState("");
  const [selectedEmoji, setSelectedEmoji] = useState("📌");
  const [showPicker, setShowPicker] = useState(false);
  const [editingGoalId, setEditingGoalId] = useState<string | null>(null);

  // Add Goal
  const handleAddGoal = () => {
    if (!title.trim()) return;

    dispatch(
      addGoal({
        id: Date.now().toString(),
        title,
        completed: false,
        icon: selectedEmoji,
      })
    );

    setTitle("");
    setSelectedEmoji("📌");
  };

  // Emoji Select
  const onEmojiSelect = (emoji: EmojiData) => {
    const selected = (emoji as any).native;

    if (editingGoalId) {
      dispatch(updateGoalIcon({ id: editingGoalId, icon: selected }));
      setEditingGoalId(null);
    } else {
      setSelectedEmoji(selected);
    }

    setShowPicker(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>🎯 Goal Manager</h2>

      {/* Add Goal Section */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter goal..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ padding: "8px", marginRight: "10px" }}
        />

        <button onClick={() => setShowPicker(!showPicker)}>
          {selectedEmoji}
        </button>

        <button
          onClick={handleAddGoal}
          style={{ marginLeft: "10px", padding: "8px" }}
        >
          Add Goal
        </button>

        {showPicker && (
          <div style={{ position: "absolute", zIndex: 1000 }}>
            <Picker onSelect={onEmojiSelect} />
          </div>
        )}
      </div>

      {/* Goals List */}
      <div>
        {goals.map((goal) => (
          <div
            key={goal.id}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div>
              <span style={{ fontSize: "20px", marginRight: "10px" }}>
                {goal.icon || "📌"}
              </span>
              {goal.title}
            </div>

            <button
              onClick={() => {
                setEditingGoalId(goal.id);
                setShowPicker(true);
              }}
            >
              Change Icon
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GoalManager;