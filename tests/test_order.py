from __future__ import absolute_import, division, print_function

import pytest

from symantecssl.exceptions import SymantecError
from symantecssl.order import (
    Order, GetOrderByPartnerOrderID, ModifyOrder, ValidateOrderParameters
)


def test_order_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <QuickOrder>
        <OrderResponseHeader>
            <PartnerOrderID>1234</PartnerOrderID>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
        <GeoTrustOrderID>abcdefg</GeoTrustOrderID>
    </QuickOrder>
    """.strip()

    assert Order().response(xml) == {
        "PartnerOrderID": "1234",
        "GeoTrustOrderID": "abcdefg",
    }


def test_order_response_failure():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <QuickOrder>
        <OrderResponseHeader>
            <Errors>
                <Error>
                    <ErrorMessage>An Error!</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>1</SuccessCode>
        </OrderResponseHeader>
    </QuickOrder>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        Order().response(xml)

    assert exc_info.value.args == (
        "There was an error submitting this SSL certificate: 'An Error!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error!"}]


def test_get_order_by_partner_order_id_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrderByPartnerOrderID>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:36:43.318+0000</Timestamp>
            <SuccessCode>0</SuccessCode>
            <ReturnCount>1</ReturnCount>
        </QueryResponseHeader>
        <OrderDetail>
            <OrderInfo>
                <Method>RESELLER</Method>
                <DomainName>testingsymantecssl.com</DomainName>
                <ProductCode>SSL123</ProductCode>
                <PartnerOrderID>1234</PartnerOrderID>
                <ServerCount>1</ServerCount>
                <ValidityPeriod>12</ValidityPeriod>
                <OrderStatusMajor>PENDING</OrderStatusMajor>
                <OrderState>WF_DOMAIN_APPROVAL</OrderState>
                <OrderDate>2014-05-29T17:36:39.000+0000</OrderDate>
                <RenewalInd>N</RenewalInd>
                <Price>35</Price>
                <GeoTrustOrderID>1806482</GeoTrustOrderID>
            </OrderInfo>
        </OrderDetail>
    </GetOrderByPartnerOrderID>
    """.strip()

    assert GetOrderByPartnerOrderID().response(xml) == {
        "OrderStatusMajor": "PENDING",
        "GeoTrustOrderID": "1806482",
        "DomainName": "testingsymantecssl.com",
        "ProductCode": "SSL123",
        "ValidityPeriod": "12",
        "OrderDate": "2014-05-29T17:36:39.000+0000",
        "Price": "35",
        "RenewalInd": "N",
        "Method": "RESELLER",
        "PartnerOrderID": "1234",
        "OrderState": "WF_DOMAIN_APPROVAL",
        "ServerCount": "1",
    }


def test_get_order_by_partner_order_id_response_failure():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrderByPartnerOrderID>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:49:18.880+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorMessage>An Error Message!</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>-1</SuccessCode>
            <ReturnCount>0</ReturnCount>
        </QueryResponseHeader>
    <OrderDetail/>
    </GetOrderByPartnerOrderID>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        GetOrderByPartnerOrderID().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error getting the order details: 'An Error Message!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!"}]


def test_modify_order_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ModifyOrder>
        <OrderResponseHeader>
            <Timestamp>2014-05-19T12:38:01.835+0000</Timestamp>
            <PartnerOrderID>OxJL7QuR2gyX7LiQHJun0</PartnerOrderID>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
    </ModifyOrder>
    """.strip()

    assert ModifyOrder().response(xml) is None


def test_modify_order_response_error():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ModifyOrder>
        <OrderResponseHeader>
            <Timestamp>2014-05-19T12:35:45.250+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorMessage>An Error Message!!</ErrorMessage>
                </Error>
            </Errors>
            <PartnerOrderID>1234</PartnerOrderID>
            <SuccessCode>-1</SuccessCode>
        </OrderResponseHeader>
    </ModifyOrder>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        ModifyOrder().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error modifying the order: 'An Error Message!!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!!"}]


def test_validate_order_parameters_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ValidateOrderParameters>
        <ValidityPeriod>12</ValidityPeriod>
        <Price>$35 USD</Price>
        <OrderResponseHeader>
            <Timestamp>2014-06-16T16:55:58.611+0000</Timestamp>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
        <ParsedCSR>
            <State>Texas</State>
            <Country>US</Country>
            <DomainName>testingsymantecssl.com</DomainName>
            <EncryptionAlgorithm>RSA</EncryptionAlgorithm>
            <Locality>San Antonio</Locality>
            <Organization>Test</Organization>
            <Email/>
            <HashAlgorithm>SHA1</HashAlgorithm>
            <OrganizationUnit/>
            <IsValidTrueDomainName>true</IsValidTrueDomainName>
            <IsValidQuickDomainName>true</IsValidQuickDomainName>
            <HasBadExtensions>false</HasBadExtensions>
        </ParsedCSR>
        <CertificateSignatureHashAlgorithm>SHA1</CertificateSignatureHashAlgorithm>
    </ValidateOrderParameters>
    """.strip()

    assert ValidateOrderParameters().response(xml) == {
        "ValidityPeriod": "12",
        "Price": "$35 USD",
        "ParsedCSR": {
            "State": "Texas",
            "Country": "US",
            "DomainName": "testingsymantecssl.com",
            "EncryptionAlgorithm": "RSA",
            "Locality": "San Antonio",
            "Organization": "Test",
            "Email": None,
            "HashAlgorithm": "SHA1",
            "OrganizationUnit": None,
            "IsValidTrueDomainName": "true",
            "IsValidQuickDomainName": "true",
            "HasBadExtensions": "false",
        },
        "CertificateSignatureHashAlgorithm": "SHA1",
    }


def test_validate_order_parameters_error():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ValidateOrderParameters>
        <ValidityPeriod>0</ValidityPeriod>
        <OrderResponseHeader>
            <Timestamp>2014-06-16T16:54:34.260+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorCode>-2019</ErrorCode>
                    <ErrorField>ValidityPeriod</ErrorField>
                    <ErrorMessage>Validity period not valid</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>-1</SuccessCode>
        </OrderResponseHeader>
        <ParsedCSR>
            <State>Texas</State>
            <Country>US</Country>
            <DomainName>testingsymantecssl.com</DomainName>
            <EncryptionAlgorithm>RSA</EncryptionAlgorithm>
            <Locality>San Antonio</Locality>
            <Organization>Test</Organization>
            <Email/>
            <HashAlgorithm>SHA1</HashAlgorithm>
            <OrganizationUnit/>
            <IsValidTrueDomainName>true</IsValidTrueDomainName>
            <IsValidQuickDomainName>true</IsValidQuickDomainName>
            <HasBadExtensions>false</HasBadExtensions>
        </ParsedCSR>
        <CertificateSignatureHashAlgorithm>SHA1</CertificateSignatureHashAlgorithm>
    </ValidateOrderParameters>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        ValidateOrderParameters().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error validating the order parameters: "
        "'Validity period not valid'",
    )
    assert exc_info.value.errors == [{
        "ErrorCode": "-2019",
        "ErrorField": "ValidityPeriod",
        "ErrorMessage": "Validity period not valid",
    }]
