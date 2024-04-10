import { styled } from "@styled-system/jsx";

export const Button = styled("button", {
  base: {
    padding: "0.4rem 1rem",
    fontSize: "1rem",
    borderRadius: "0.4rem",
    border: "1px solid #e0e0e0",
    backgroundColor: "#f5f5f5",
    _disabled: {
      backgroundColor: "#f0f0f0",
      color: "#a0a0a0",
    },
  },
  variants: {
    primary: {
      true: {
        backgroundColor: "blue",
        color: "white",
        _hover: {
          backgroundColor: "darkblue",
        },
      },
    },
  },
});
