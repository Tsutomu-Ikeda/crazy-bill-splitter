import {
  Avatar,
  Button,
  Card,
  Container,
  Heading,
  Label,
  Form,
  Input,
} from "@/components/ui";
import { clsx } from "clsx";
// import { DataTableDemo } from "@/components/organisms/table";
// import { Button } from "@/components/ui/button";
// import { Select, Form, Avatar } from "@/components/ui";
import { TriangleRightIcon } from "@radix-ui/react-icons";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import type { MetaFunction } from "@remix-run/node";
import { Await, useAsyncValue, useLoaderData } from "@remix-run/react";
import { css } from "@styled-system/css";
import {
  DetailedHTMLProps,
  HTMLAttributes,
  Suspense,
  useEffect,
  useMemo,
  useState,
} from "react";
import { z } from "zod";

export const meta: MetaFunction = () => {
  return [{ title: "詳細" }, { name: "description", content: "詳細" }];
};

const formSchema = z.object({
  title: z.string().min(1),
  amount: z.number().min(1).max(100000),
  paid_by: z.string(),
  paid_for: z.array(z.string()),
});

const ShowSettlements = (
  props: DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement>
) => {
  const { settlements }: any = useAsyncValue();

  return (
    <div
      {...props}
      className={css({
        padding: "0.5rem 1rem 1rem 1rem",
        borderRadius: "8px",
        border: "1px solid #ddd",
        backgroundColor: "#FFF",
      })}
    >
      <h2
        className={css({
          padding: "0 0.5rem 0.5rem 0.5rem",
          fontSize: "1.2rem",
          color: "#666",
          width: "fit-content",
          borderRadius: 8,
        })}
      >
        精算金額
      </h2>
      <div
        className={clsx(
          css({
            display: "grid",
            gap: "1rem",
            gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
            gridAutoRows: "min-content",
            overflow: "scroll",
            paddingBottom: "0.5rem",
          }),
          props.className
        )}
      >
        {settlements.map((settlement: any, index: any) => {
          const formatted = new Intl.NumberFormat("ja-JP", {
            style: "currency",
            currency: "JPY",
          }).format(settlement.amount);

          return (
            <Card.Root key={index}>
              <Card.Title flexGrow className={css({ height: 8 })}>
                <div
                  className={css({
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "0.1rem",
                  })}
                >
                  <Avatar.Root
                    className={css({
                      height: 8,
                      width: 8,
                    })}
                  >
                    <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                    <Avatar.Fallback
                      style={{ backgroundColor: settlement.send_by.color }}
                    >
                      {settlement.send_by.name}
                    </Avatar.Fallback>
                  </Avatar.Root>
                  <TriangleRightIcon />
                  <Avatar.Root
                    className={css({
                      height: 8,
                      width: 8,
                    })}
                  >
                    <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                    <Avatar.Fallback
                      style={{ backgroundColor: settlement.send_for.color }}
                    >
                      {settlement.send_for.name}
                    </Avatar.Fallback>
                  </Avatar.Root>
                </div>
                <div
                  className={css({
                    marginLeft: "auto",
                    fontWeight: "bold",
                  })}
                >
                  {formatted}
                </div>
              </Card.Title>
            </Card.Root>
          );
        })}
      </div>
    </div>
  );
};

interface LoaderData {
  participants: {
    name: string;
    fullName: string;
    email?: string;
    color?: string;
  }[];
  payments: {
    title: string;
    amount: number;
    paid_by: { name: string; color?: string };
    paid_for: { name: string; color?: string }[];
  }[];
}

export const clientLoader = ({ params }): LoaderData => {
  const sessionId = params.sessionId;

  console.log("sessionId", sessionId);

  const participants = [
    {
      name: "A",
      color: "#FF6347",
      email: "alice@tomtsutom.com",
      fullName: "Alice Johnson",
    },
    {
      name: "B",
      color: "#2CA02C",
      email: "bob.smith@tomtsuto.com",
      fullName: "Bob Smith",
    },
    { name: "C", color: "#4169E1", fullName: "Charlie Brown" },
    { name: "D", color: "#FF8C00", fullName: "David Wilson" },
    { name: "E", color: "#9370DB", fullName: "Eve Miller" },
    { name: "F", color: "#FF6347", fullName: "Franklin Davis" },
    { name: "G", color: "#2CA02C", fullName: "Grace Lee" },
    { name: "H", color: "#4169E1", fullName: "Henry Young" },
    { name: "I", color: "#FF8C00", fullName: "Isabella Scott" },
    { name: "J", color: "#9370DB", fullName: "Jack Wright" },
    { name: "K", color: "#FF6347", fullName: "Katherine Lopez" },
    { name: "L", color: "#2CA02C", fullName: "Liam Hill" },
    { name: "M", color: "#4169E1", fullName: "Mia Green" },
    { name: "N", color: "#FF8C00", fullName: "Noah Adams" },
    { name: "O", color: "#9370DB", fullName: "Olivia Baker" },
    { name: "P", color: "#FF6347", fullName: "Patrick Campbell" },
    { name: "Q", color: "#2CA02C", fullName: "Quinn Carter" },
    { name: "R", color: "#4169E1", fullName: "Riley Hall" },
    { name: "S", color: "#FF8C00", fullName: "Sophia Allen" },
    { name: "T", color: "#9370DB", fullName: "Thomas Young" },
  ];

  const payments = [
    {
      title: "hoge代",
      amount: 13000,
      paid_by: { name: "A", color: "#FF6347" },
      paid_for: participants,
    },
    {
      title: "fuga代",
      amount: 12000,
      paid_by: { name: "B", color: "#2CA02C" },
      paid_for: participants,
    },
    {
      title: "piyo代",
      amount: 11500,
      paid_by: { name: "C", color: "#4169E1" },
      paid_for: participants,
    },
    {
      title: "foo代",
      amount: 6000,
      paid_by: { name: "D", color: "#FF8C00" },
      paid_for: participants,
    },
    {
      title: "bar代",
      amount: 2500,
      paid_by: { name: "E", color: "#9370DB" },
      paid_for: [
        { name: "A", color: "#FF6347" },
        { name: "B", color: "#2CA02C" },
        { name: "C", color: "#4169E1" },
        { name: "D", color: "#FF8C00" },
        { name: "E", color: "#9370DB" },
      ],
    },
  ];

  return { participants, payments };
};

export default function Index() {
  const { participants, payments: defaultPayment } =
    useLoaderData<LoaderData>();
  const [payments, setPayments] = useState(defaultPayment);

  const settlementsPromise = useMemo(() => {
    const host = window.location.host.replace("5174", "8080");
    return fetch(`http://${host}/calculate-settlements`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ participants, payments }),
    })
      .then((res) => res.json())
      .then(({ settlements }) => {
        return {
          settlements: settlements.map((settlement: any) => {
            const send_by = participants.find(
              (participant) => participant.name === settlement.send_by.name
            );
            const send_for = participants.find(
              (participant) => participant.name === settlement.send_for.name
            );

            return {
              ...settlement,
              send_by,
              send_for,
            };
          }),
        };
      });
  }, [participants, payments]);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      amount: 0,
      paid_by: "A",
      paid_for: ["A", "B", "C", "D", "E"],
    },
  });

  // function onSubmit(values: z.infer<typeof formSchema>) {
  //   setPayments((prev) => [
  //     ...prev,
  //     {
  //       title: values.title,
  //       amount: values.amount,
  //       paid_by: {
  //         name: values.paid_by,
  //         color: participants.find((p) => p.name === values.paid_by)?.color,
  //       },
  //       paid_for: values.paid_for.map((name) => {
  //         const participant = participants.find((p) => p.name === name);

  //         if (!participant) {
  //           return { name };
  //         }

  //         return {
  //           name: participant.name,
  //           color: participant.color,
  //         };
  //       }),
  //     },
  //   ]);
  // }

  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  });

  const hogeParticipants = [
    {
      name: "ゆこさん",
      支出額: 7102,
      支払済額: 0,
    },
    {
      name: "あっすーさん",
      支出額: 9168,
      支払済額: 0,
    },
    {
      name: "なりたさん",
      支出額: 9168,
      支払済額: 17000,
    },
    {
      name: "issan",
      支出額: 9168,
      支払済額: 2400,
    },
    {
      name: "にし",
      支出額: 7102,
      支払済額: 22310,
    }
  ]

  return (
    <Container
      className={css({
        fontFamily: "system-ui, sans-serif",
        width: "95vw",
        margin: "auto",
        display: "flex",
        gap: 10,
        maxWidth: 1280,
        paddingBottom: 12,
      })}
    >
      <Heading.Top>Crazy Bill Splitter</Heading.Top>
      <div style={{
        padding: "0.5rem 1rem 1rem 1rem",
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
        gap: "1rem",
      }}>
        {hogeParticipants.map((participant, index) => (
          <Card.Root key={index}>
            <Card.Title flexGrow style={{ height: 48 }}>
              <div className={css({ display: "grid" })}>
                <Label ellipsis>{participant.name}: {Math.abs(participant.支払済額 - participant.支出額)}円 {participant.支払済額 > participant.支出額 ? "受取" : "支払"}</Label>
                <Card.Subtitle>
                  <Label ellipsis>
                    支払済額: {participant.支払済額}円 /
                    支出額: {participant.支出額}円
                  </Label>
                </Card.Subtitle>
              </div>
            </Card.Title>
          </Card.Root>
        ))}
      </div>

      <div style={{
        height: "200px"
      }}></div>

      <div
        className={css({
          padding: "0.5rem 1rem 1rem 1rem",
          borderRadius: "8px",
          border: "1px solid #ddd",
          backgroundColor: "#FFF",
        })}
      >
        <h2
          className={css({
            padding: "0 0.5rem 0.5rem 0.5rem",
            fontSize: "1.2rem",
            color: "#666",
            width: "fit-content",
            borderRadius: 8,
          })}
        >
          参加者
          <span className={css({ fontSize: "0.9rem" })}>
            {participants.length > 0 && ` ${participants.length}名`}
          </span>
        </h2>
        {isMobile ? (
          <Avatar.Group
            className={css({
              padding: "0 1rem",
              overflowX: "scroll",
            })}
          >
            {participants.map((participant) => (
              <Avatar.Root key={participant.name}>
                <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                <Avatar.Fallback style={{ backgroundColor: participant.color }}>
                  {participant.name}
                </Avatar.Fallback>
              </Avatar.Root>
            ))}
          </Avatar.Group>
        ) : (
          <div
            className={css({
              display: "grid",
              gap: "1rem",
              gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
              gridAutoRows: "min-content",
              maxHeight: "130px",
              overflow: "scroll",
              paddingBottom: "0.5rem",
            })}
          >
            {participants.map((participant, index) => (
              <Card.Root key={index}>
                <Card.Title flexGrow style={{ height: 48 }}>
                  <Avatar.Root>
                    <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                    <Avatar.Fallback
                      style={{ backgroundColor: participant.color }}
                    >
                      {participant.name}
                    </Avatar.Fallback>
                  </Avatar.Root>
                  <div className={css({ display: "grid" })}>
                    <Label ellipsis>{participant.fullName}</Label>
                    <Card.Subtitle>
                      <Label ellipsis>{participant.email}</Label>
                    </Card.Subtitle>
                  </div>
                </Card.Title>
              </Card.Root>
            ))}
          </div>
        )}
      </div>

      <div
        className={css({
          display: "flex",
          flexDirection: "column",
          gap: 4,
          marginBottom: 4,
          "@media (min-width: 768px)": {
            flexDirection: "row",
          },
        })}
      >
        <div
          className={css({
            width: "100%",
            padding: "0.5rem 1rem",
            borderRadius: 8,
            backgroundColor: "#FFF",
            border: "1px solid #ddd",
            "@media (min-width: 768px)": {
              width: "60%",
              padding: "1rem",
            },
          })}
        >
          <div
            className={css({
              height: 500,
              overflowY: "scroll",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            })}
          >
            <Form.Root {...form}>
              <Form.Field name="amount">
                <Form.Label>金額</Form.Label>
                <Form.Control asChild>
                  <Input
                    type="number"
                    onChange={(e) => {
                      form.setValue("amount", Number(e.target.value));
                    }}
                  />
                </Form.Control>
              </Form.Field>
              <Form.Field name="title">
                <Form.Item>
                  <Form.Label>タイトル</Form.Label>
                  <Input type="text" />
                </Form.Item>
              </Form.Field>
              <Form.Field name="paid_by">
                <Form.Label>支払者</Form.Label>
                {/* <Select.Root
                  onValueChange={(value) => {
                    form.setValue("paid_by", value);
                  }}
                  buttonElementHeight="46px"
                >
                  <Select.Trigger id="paid_by">
                    <Select.Value placeholder="Select" />
                  </Select.Trigger>
                  <Select.Content>
                    {participants.map((participant, index) => (
                      <Select.Item key={index} value={participant.name}>
                        <div className="flex p-1 items-center">
                          <Avatar.Root className="h-9 w-9">
                            <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                            <Avatar.Fallback
                              style={{
                                backgroundColor: participant.color,
                              }}
                            >
                              {participant.name}
                            </Avatar.Fallback>
                          </Avatar.Root>
                          <div className="ml-4 space-y-1 overflow-hidden">
                            <p className="text-sm font-medium leading-none">
                              {participant.fullName}
                            </p>
                            <p className="text-sm text-muted-foreground text-ellipsis overflow-hidden">
                              {participant.email}
                            </p>
                          </div>
                        </div>
                      </Select.Item>
                    ))}
                  </Select.Content>
                </Select.Root> */}
              </Form.Field>
              <Form.Field name="paid_for">
                <Form.Label>精算対象者</Form.Label>
                <Avatar.Group
                  className={css({
                    padding: "0 1rem",
                    overflowX: "scroll",
                  })}
                >
                  {participants.map((participant, index) => (
                    <Avatar.Root key={index}>
                      <Avatar.Image src="/avatars/01.png" alt="Avatar" />
                      <Avatar.Fallback
                        style={{
                          backgroundColor: participant.color,
                        }}
                      >
                        {participant.name}
                      </Avatar.Fallback>
                    </Avatar.Root>
                  ))}
                </Avatar.Group>
              </Form.Field>
              <Button className="float-right" type="submit">
                追加
              </Button>
            </Form.Root>
          </div>
        </div>

        <div
          className={css({
            width: "100%",
            "@media (min-width: 768px)": {
              width: "40%",
            },
          })}
        >
          <Suspense fallback={<div>計算中...</div>}>
            <Await resolve={settlementsPromise}>
              <ShowSettlements
                className={css({
                  height: 500,
                  overflowY: "scroll",
                })}
              />
            </Await>
          </Suspense>
        </div>
      </div>

      {/* <DataTableDemo payments={payments} setPayments={setPayments} /> */}
    </Container >
  );
}
