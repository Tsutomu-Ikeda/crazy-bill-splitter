import { styled } from "@styled-system/jsx";

export const Input = styled("input", {
  base: {
    padding: "10px 15px",
    border: "1px solid gainsboro",
    borderRadius: 5,
    fontSize: 14,
    color: "black",
    backgroundColor: "white",
    "&:focus": {
      outline: "none",
      borderColor: "dodgerblue",
    },
  },
});
