import { styled } from "@styled-system/jsx";

export const Container = styled("div", {
  base: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    containerType: "inline-size",
  },
  variants: {
    interactive: {
      true: {
        "&:hover": {
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        },
      },
    },
  },
});
