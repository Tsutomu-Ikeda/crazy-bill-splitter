import { styled } from "@styled-system/jsx";

export const Label = styled("div", {
  base: {},
  variants: {
    ellipsis: {
      true: {
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap",
      },
    },
  },
});
