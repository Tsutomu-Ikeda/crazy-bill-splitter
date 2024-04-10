import { styled } from "@styled-system/jsx";

export const CardRoot = styled("div", {
  base: {
    display: "flex",
    flexDirection: "column",
    gap: 2,
    padding: 4,
    borderRadius: 8,
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    backgroundColor: "white",
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

export const CardHeader = styled("div", {
  base: {
    display: "flex",
    alignItems: "center",
    gap: 12,
  },
});

export const CardTitle = styled("h2", {
  base: {
    margin: 0,
    fontSize: 18,
    fontWeight: 500,
    display: "flex",
    alignItems: "center",
    gap: 4,
  },
  variants: {
    flexGrow: {
      true: {
        flexGrow: 1,
      },
    },
  },
});

export const CardSubtitle = styled("div", {
  base: {
    margin: 0,
    fontSize: 14,
    lineHeight: "1rem",
    color: "gray",
    overflow: "hidden",
  },
});

export const CardContent = styled("div", {
  base: {},
});

export const CardFooter = styled("div", {
  base: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 8,
  },
});

export const CardActions = styled("div", {
  base: {
    display: "flex",
    gap: 8,
  },
});

export const CardAction = styled("button", {
  base: {
    padding: 8,
    border: "none",
    borderRadius: 4,
    backgroundColor: "transparent",
    cursor: "pointer",
    "&:hover": {
      backgroundColor: "rgba(0, 0, 0, 0.05)",
    },
  },
});

export const Card = {
  Root: CardRoot,
  Header: CardHeader,
  Title: CardTitle,
  Subtitle: CardSubtitle,
  Content: CardContent,
  Footer: CardFooter,
  Actions: CardActions,
  Action: CardAction,
};
