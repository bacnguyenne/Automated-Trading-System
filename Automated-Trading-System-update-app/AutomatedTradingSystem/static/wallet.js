y$ = ()=>{
  const [e,t] = Ce.useState(W0[0])
    , [n,i] = Ce.useState(1)
    , r = zt.slice(0, 200).map(f=>f)
    , s = zt.slice(0, 61).map(f=>f)
    , o = [0, r, 0, 22]
    , a = [0, s, 0, 22]
    , l = f=>{
      t(f)
  }
    , c = new Date;
  let u = String(c.getDate()).padStart(2, "0")
    , h = String(c.getMonth() + 1).padStart(2, "0")
    , d = c.getFullYear()
    , m = `${u}/${h}/${d}`;
  return y.jsx("div", {
      className: "summaty",
      children: y.jsxs(Hr, {
          gutter: [32, 32],
          style: {
              marginTop: "40px"
          },
          children: [y.jsx(Ot, {
              className: "gutter-row",
              xs: 24,
              lg: 24,
              xl: 16,
              xxl: 18,
              children: y.jsxs("div", {
                  className: "summaty__line-chart",
                  children: [y.jsxs("div", {
                      className: "summaty__panel-line-chart",
                      children: [y.jsxs("div", {
                          children: [y.jsx("h2", {
                              children: "Performance"
                          }), y.jsx("h3", {
                              children: "$23,449.85"
                          }), y.jsx("h4", {
                              children: m
                          })]
                      }), y.jsx("div", {
                          children: ["7d", "30d"].map((f,x)=>y.jsx("button", {
                              className: n === x ? "active" : "",
                              onClick: ()=>i(x),
                              children: f
                          }, x))
                      })]
                  }), y.jsx(h$, {
                      dataChart: n ? o : a
                  })]
              })
          }), y.jsx(Ot, {
              className: "gutter-row",
              xs: 24,
              lg: 12,
              xl: 8,
              xxl: 6,
              children: y.jsxs("div", {
                  className: "doughnut-chart",
                  children: [y.jsx("h2", {
                      children: "Network allocation"
                  }), y.jsxs("div", {
                      className: "doughnut-chart__wrapper",
                      children: [y.jsx("div", {
                          className: "doughnut-chart__border"
                      }), y.jsx(d$, {
                          handleChangeLabel: l
                      }), y.jsxs("div", {
                          className: "doughnut-chart__text",
                          children: [y.jsx("h5", {
                              children: e == null ? void 0 : e.title
                          }), y.jsxs("h4", {
                              children: [e == null ? void 0 : e.procent, "%"]
                          })]
                      })]
                  }), y.jsx("ul", {
                      children: W0.map(({title: f, color: x},S)=>y.jsxs("li", {
                          onMouseEnter: ()=>t(W0[S]),
                          children: [y.jsx("span", {
                              style: x
                          }), " ", f]
                      }, S))
                  })]
              })
          }), f$.map(f=>y.jsx(Ot, {
              className: "gutter-row",
              xs: 24,
              lg: 12,
              xl: 8,
              children: y.jsx(v$, {
                  data: f
              })
          }, f.id))]
      })
  })
}
